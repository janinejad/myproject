from django.db.models import Q
from apps.catalog.models import CentralCatalogItem, BusinessCatalogOffer


class CatalogService:
    @staticmethod
    def search_similar_items(query_text: str, item_type: str, limit=5):
        """
        بررسی وجود موارد مشابه در دیتابیس مرکزی پیش از ثبت مجدد
        """
        return CentralCatalogItem.objects.filter(
            item_type=item_type
        ).filter(
            Q(title__icontains=query_text) | Q(description__icontains=query_text)
        )[:limit]

    @classmethod
    def attach_or_create_product(cls, business, title: str, item_type: str, category, price=None, custom_desc=""):
        """
        اتصال محصول به کسب‌وکار یا ایجاد آیتم جدید در کاتالوگ مرکزی
        """
        catalog_item, created = CentralCatalogItem.objects.get_or_create(
            title=title.strip(),
            item_type=item_type,
            defaults={'category': category, 'is_verified': False}
        )

        offer = BusinessCatalogOffer.objects.create(
            business=business,
            catalog_item=catalog_item,
            price=price,
            custom_description=custom_desc
        )
        return offer