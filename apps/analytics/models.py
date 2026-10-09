import logging
from django.conf import settings
from django.db import transaction
from django.db.models import F
import redis

logger = logging.getLogger(__name__)

# دریافت آدرس Redis با مقدار پیش‌فرض ایمن جهت جلوگیری از AttributeError
REDIS_URL = getattr(settings, 'REDIS_URL', 'redis://127.0.0.1:6379/0')

try:
    redis_client = redis.Redis.from_url(REDIS_URL)
except Exception as e:
    logger.error(f"خطا در اتصال به Redis: {e}")
    redis_client = None


class AnalyticsService:
    REDIS_COUNTER_KEY = "business_views_counter"
    DEDUP_TTL_SECONDS = 86400  # ۲۴ ساعت

    @classmethod
    def record_view(cls, business_id: int, user_ip: str) -> bool:
        if not redis_client or not user_ip:
            return False

        try:
            dedup_key = f"view_dedup:{business_id}:{user_ip}"
            is_new_view = redis_client.set(dedup_key, "1", ex=cls.DEDUP_TTL_SECONDS, nx=True)

            if is_new_view:
                redis_client.hincrby(cls.REDIS_COUNTER_KEY, business_id, 1)
                return True

            return False
        except Exception as e:
            logger.error(f"خطا در ثبت بازدید Redis برای کسب‌وکار شناسه {business_id}: {e}")
            return False

    @classmethod
    def sync_views_to_db(cls) -> int:
        if not redis_client:
            return 0

        from apps.businesses.models import Business

        updated_businesses_count = 0
        try:
            raw_counters = redis_client.hgetall(cls.REDIS_COUNTER_KEY)
            if not raw_counters:
                return 0

            with transaction.atomic():
                for b_id_bytes, count_bytes in raw_counters.items():
                    business_id = int(b_id_bytes.decode('utf-8'))
                    increment_val = int(count_bytes.decode('utf-8'))

                    if increment_val > 0:
                        rows_affected = Business.objects.filter(id=business_id).update(
                            views_count=F('views_count') + increment_val
                        )

                        if rows_affected > 0:
                            redis_client.hincrby(cls.REDIS_COUNTER_KEY, business_id, -increment_val)
                            updated_businesses_count += 1

            return updated_businesses_count
        except Exception as e:
            logger.error(f"خطا هنگام همگام‌سازی آمار بازدید از Redis به دیتابیس: {e}")
            return 0