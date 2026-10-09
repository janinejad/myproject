from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from apps.businesses.views import HomeView, BusinessDetailView
from apps.businesses.api.views import BusinessViewSet
from apps.search.views import live_search_api

# روتر مربوط به REST API
router = DefaultRouter()
router.register(r'businesses', BusinessViewSet, basename='api-businesses')

urlpatterns = [
    # ۱. صفحات وب فرانت‌اند (Website Routes)
    path('', HomeView.as_view(), name='home'),
    path('businesses/<slug:slug>/', BusinessDetailView.as_view(), name='business_detail'),

    # ۲. پنل مدیریت
    path('admin/', admin.site.urls),

    # ۳. مسیرهای REST API (مخصوص اپلیکیشن موبایل و React/Flutter در آینده)
    path('api/v1/', include(router.urls)),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/v1/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/v1/search/live/', live_search_api, name='api_live_search'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
