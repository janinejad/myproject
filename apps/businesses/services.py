from django.db import transaction
from django.utils.text import slugify
from .models import Business, BusinessStatus


class BusinessService:
    @staticmethod
    @transaction.atomic
    def create_business(*, owner, title, category, description, address, phone="", mobile="", cover_image=None,
                        logo=None):
        """
        منطق ثبت کسب‌وکار جدید - مشترک بین API و Web View
        """
        slug = slugify(title, allow_unicode=True)

        # اطمینان از یکتا بودن slug
        base_slug = slug
        counter = 1
        while Business.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        business = Business.objects.create(
            owner=owner,
            title=title,
            slug=slug,
            category=category,
            description=description,
            address=address,
            phone=phone,
            mobile=mobile,
            cover_image=cover_image,
            logo=logo,
            status=BusinessStatus.PENDING
        )

        # در صورت نیاز: ارسال نوتيفیکیشن به مدیر یا اجرای رویدادهای جانبی
        return business

    @staticmethod
    def approve_business(business_id: int, admin_user):
        """
        تأیید کسب‌وکار توسط مدیر
        """
        business = Business.objects.get(id=business_id)
        business.status = BusinessStatus.APPROVED
        business.save()
        return business