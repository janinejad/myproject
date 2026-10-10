from django.db import models
from django.conf import settings
from apps.categories.models import Category
from django.urls import reverse

class BusinessStatus(models.TextChoices):
    PENDING = 'pending', 'در انتظار بررسی'
    APPROVED = 'approved', 'تأیید شده'
    REJECTED = 'rejected', 'رد شده'
    SUSPENDED = 'suspended', 'معلق شده'


class Business(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='businesses')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='primary_businesses')
    sub_categories = models.ManyToManyField(Category, blank=True, related_name='secondary_businesses')

    title = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, allow_unicode=True)
    description = models.TextField()

    logo = models.ImageField(upload_to='businesses/logos/', null=True, blank=True)
    cover_image = models.ImageField(upload_to='businesses/covers/', null=True,
                                    blank=True)  # هدر مشابه Facebook

    address = models.TextField()
    phone = models.CharField(max_length=30)
    mobile = models.CharField(max_length=30, blank=True)
    website = models.URLField(blank=True)

    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    status = models.CharField(max_length=20, choices=BusinessStatus.choices, default=BusinessStatus.PENDING)
    is_active = models.BooleanField(default=True)
    views_count = models.PositiveIntegerField(default=0, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('business_detail', kwargs={'slug': self.slug})


class BusinessWorkingHour(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='working_hours')
    day_of_week = models.IntegerField(choices=[(i, str(i)) for i in range(7)])  # 0: شنبه تا 6: جمعه
    open_time = models.TimeField()
    close_time = models.TimeField()
    is_closed = models.BooleanField(default=False)


class BusinessSocial(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='social_links')
    platform = models.CharField(max_length=50)  # Instagram, Telegram, LinkedIn
    url = models.URLField()