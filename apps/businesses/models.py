from django.db import models
from django.conf import settings
from apps.core.models import TimeStampedModel
from apps.categories.models import Category


class BusinessStatus(models.TextChoices):
    PENDING = 'pending', 'در انتظار تأیید'
    APPROVED = 'approved', 'تأیید شده'
    REJECTED = 'rejected', 'رد شده'
    SUSPENDED = 'suspended', 'معلق شده'


class Business(TimeStampedModel):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='businesses')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='primary_businesses')
    sub_categories = models.ManyToManyField(Category, blank=True, related_name='secondary_businesses')

    title = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=280, unique=True, allow_unicode=True)
    description = models.TextField()

    logo = models.ImageField(upload_to='businesses/logos/', null=True, blank=True)
    cover_image = models.ImageField(upload_to='businesses/covers/', null=True, blank=True)

    phone = models.CharField(max_length=20, blank=True)
    mobile = models.CharField(max_length=20, blank=True)
    website = models.URLField(blank=True)
    address = models.TextField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    status = models.CharField(max_length=20, choices=BusinessStatus.choices, default=BusinessStatus.PENDING)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title