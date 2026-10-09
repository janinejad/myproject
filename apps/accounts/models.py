from django.contrib.auth.models import AbstractUser
from django.db import models

class UserRole(models.TextChoices):
    USER = 'user', 'کاربر عادی'
    BUSINESS_OWNER = 'business_owner', 'صاحب کسب‌وکار'
    MODERATOR = 'moderator', 'مدیر محتوا'
    ADMIN = 'admin', 'مدیر سیستم'
    SUPER_ADMIN = 'super_admin', 'مدیر ارشد'

class User(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True, db_index=True)
    role = models.CharField(max_length=20, choices=UserRole.choices, default=UserRole.USER)
    is_verified = models.BooleanField(default=False)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)