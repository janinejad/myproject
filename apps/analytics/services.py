import redis
from django.conf import settings
from django.db.models import F



r = redis.Redis.from_url(settings.REDIS_URL,protocol=2)


class AnalyticsService:
    @staticmethod
    def record_view(business_id: int, user_ip: str):
        # کلید یکتای کاربر برای جلوگیری از شمارش تکراری در 24 ساعت
        dedup_key = f"view_dedup:{business_id}:{user_ip}"

        if not r.get(dedup_key):
            r.setex(dedup_key, 86400, "1")  # انقضا ۲۴ ساعت
            # افزایش شمارنده در Redis
            r.hincrby("business_views_counter", business_id, 1)

    @staticmethod
    def sync_views_to_db():
        """
        تسک دوره‌ای Celery جهت انتقال اعداد متراکم‌شده از Redis به PostgreSQL
        """
        counters = r.hgetall("business_views_counter")
        from apps.businesses.models import Business

        for b_id, count in counters.items():
            business_id = int(b_id.decode('utf-8'))
            inc_val = int(count.decode('utf-8'))

            Business.objects.filter(id=business_id).update(
                views_count=F('views_count') + inc_val
            )
            r.hincrby("business_views_counter", business_id, -inc_val)