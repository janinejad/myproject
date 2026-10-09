from apps.businesses.models import Business, BusinessStatus
from apps.analytics.services import AnalyticsService


class BusinessService:
    @staticmethod
    def get_approved_businesses():
        return Business.objects.filter(status=BusinessStatus.APPROVED, is_active=True).select_related('category')

    @staticmethod
    def get_business_detail(slug_or_id, request_ip=None):
        business = Business.objects.prefetch_related(
            'working_hours', 'social_links', 'offers__catalog_item', 'comments__replies'
        ).get(slug=slug_or_id, status=BusinessStatus.APPROVED)

        # ثبت غیرهمزمان بازدید
        if request_ip:
            AnalyticsService.record_view(business.id, request_ip)

        return business

    @staticmethod
    def get_related_businesses(business, limit=4):
        """
        دریافت کسب‌وکارهای مرتبط بر اساس دسته‌بندی و زیردسته‌بندی مشترک
        """
        return Business.objects.filter(
            status=BusinessStatus.APPROVED,
            category=business.category
        ).exclude(id=business.id)[:limit]