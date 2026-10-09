from django.db import models
from apps.businesses.models import Business
from apps.categories.models import Category

class ItemType(models.TextChoices):
    PRODUCT = 'product', 'کالا'
    SERVICE = 'service', 'خدمت'

# موجودیت مرکزی کاتالوگ (جلوگیری از ثبت تکراری)
class CentralCatalogItem(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    item_type = models.CharField(max_length=10, choices=ItemType.choices)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='catalog_items')
    description = models.TextField(blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('title', 'item_type')

# جدول واسط متصل‌کننده کسب‌وکار به کاتالوگ مرکزی همراه با مشخصات اختصاصی
class BusinessCatalogOffer(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='offers')
    catalog_item = models.ForeignKey(CentralCatalogItem, on_delete=models.CASCADE, related_name='business_offers')
    custom_title = models.CharField(max_length=255, blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=0, null=True, blank=True)
    is_available = models.BooleanField(default=True)
    custom_description = models.TextField(blank=True)
    purchase_link = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)