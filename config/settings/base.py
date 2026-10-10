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
    'import_export',
    'django_ckeditor_5',
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
JALALI_DATE_DEFAULTS = {
    # if change it to true then all dates of the list_display will convert to the Jalali.
    'LIST_DISPLAY_AUTO_CONVERT': False,
    'Strftime': {
        'date': '%y/%m/%d',
        'datetime': '%H:%M:%S _ %y/%m/%d',
    },
    'Static': {
        'js': [
            'admin/js/django_jalali.min.js',
        ],
        'css': {
            'all': [
                'admin/css/django_jalali.min.css',
            ]
        }
    },
}

# تنظیمات کامل و پیشرفته CKEditor 5
CKEDITOR_5_CONFIGS = {
    'default': {
        'toolbar': [
            'heading', '|',
            'bold', 'italic', 'underline', 'strikethrough', 'subscript', 'superscript', '|',
            'fontColor', 'fontBackgroundColor', 'fontSize', 'fontFamily', '|',
            'alignment', '|',
            'bulletedList', 'numberedList', 'todoList', 'outdent', 'indent', '|',
            'link', 'uploadImage', 'insertTable', 'blockQuote', 'codeBlock', 'mediaEmbed', '|',
            'removeFormat', 'sourceEditing'
        ],
        'image': {
            'toolbar': [
                'imageTextAlternative', 'imageStyle:inline', 'imageStyle:block', 'imageStyle:side', '|',
                'toggleImageCaption'
            ]
        },
        'table': {
            'contentToolbar': [
                'tableColumn', 'tableRow', 'mergeTableCells', 'tableCellProperties', 'tableProperties'
            ]
        },
        'heading': {
            'options': [
                {'model': 'paragraph', 'title': 'Paragraph', 'class': 'ck-heading_paragraph'},
                {'model': 'heading1', 'view': 'h1', 'title': 'Heading 1', 'class': 'ck-heading_h1'},
                {'model': 'heading2', 'view': 'h2', 'title': 'Heading 2', 'class': 'ck-heading_h2'},
                {'model': 'heading3', 'view': 'h3', 'title': 'Heading 3', 'class': 'ck-heading_h3'},
                {'model': 'heading4', 'view': 'h4', 'title': 'Heading 4', 'class': 'ck-heading_h4'}
            ]
        },
        'language': 'fa', # پشتیبانی کامل از زبان فارسی
    }
}