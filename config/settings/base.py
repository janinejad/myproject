import os
from pathlib import Path
import sys

# مسیر ریشه پروژه
BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

# کلید امنیتی پایه
SECRET_KEY = 'django-insecure-local-dev-key-replace-in-prod'

DEBUG = True

ALLOWED_HOSTS = ['*']

# اپلیکیشن‌های نصب شده
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party Apps
    'rest_framework',
    'rest_framework_simplejwt',
    'drf_spectacular',
    'mptt',

    # Local Apps
    'apps.core',
    'apps.accounts',
    'apps.categories',
    'apps.businesses',
    'apps.catalog',
    'apps.engagement',
    'apps.analytics',
    'apps.search',
    'apps.ai_integration',
]

# میدل‌ورها
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# تنظیمات اصلی مسیردهی URLs (رفع خطای ROOT_URLCONF)
ROOT_URLCONF = 'config.urls'

# تنظیمات قالب‌ها
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# مدل کاربر اختصاصی
AUTH_USER_MODEL = 'accounts.User'

# تنظیمات فایل‌های استاتیک و رسانه (رفع خطای STATIC_URL)
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# تنظیمات پیش‌فرض برای Primary Keyها
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
REDIS_URL = 'redis://127.0.0.1:6379/0'