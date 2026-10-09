
from rest_framework import viewsets, permissions
from apps.businesses.models import Business
from apps.businesses.api.serializers import BusinessSerializer
from apps.businesses.services import BusinessService

class BusinessViewSet(viewsets.ModelViewSet):
    queryset = Business.objects.filter(is_active=True)
    serializer_class = BusinessSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        # استفاده مستقیم از منطق مشترک لایه سرویس
        return BusinessService.get_approved_businesses()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # ثبت بازدید از طریق سرویس آنالیتیکس با Redis
        ip = request.META.get('REMOTE_ADDR')
        BusinessService.get_business_detail(instance.slug, request_ip=ip)
        return super().retrieve(request, *args, **kwargs)