from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from apps.businesses.views import BusinessViewSet

router = DefaultRouter()
router.register(r'businesses', BusinessViewSet, basename='business')

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/v1/', include(router.urls)),
    
    # Swagger Docs
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/v1/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)