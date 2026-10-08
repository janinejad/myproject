from .base import *

# فعال‌سازی حالت توسعه
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '*']

# کلید امنیتی محیط توسعه
SECRET_KEY = 'django-insecure-local-dev-key-replace-in-prod'

# تنظیمات دیتابیس محلی (PostgreSQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'my_platform_db',  # نام دیتابیس بسازید
        'USER': 'postgres',        # نام کاربری PostgreSQL
        'PASSWORD': '123',         # رمز عبور دیتابیس
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# مسیر فایل‌های آپلودی رسانه در سیستم محلی
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}