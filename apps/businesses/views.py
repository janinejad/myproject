from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Business
from .serializers import BusinessCreateSerializer, BusinessDetailSerializer
from .services import BusinessService
from django.views.generic import TemplateView, DetailView

from ..categories.models import Category


class HomeView(TemplateView):
    """View مربوط به صفحه اصلی سایت"""
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # دریافت دسته‌بندی‌های اصلی
        context['popular_categories'] = Category.objects.filter(is_active=True, parent=None)[:15]
        # دریافت برترین کسب‌وکارها از لایه سرویس
        context['top_businesses'] = BusinessService.get_approved_businesses()[:6]
        return context


class BusinessDetailView(DetailView):
    """View مربوط به صفحه اختصاصی کسب‌وکار"""
    template_name = 'businesses/business_detail.html'
    context_object_name = 'business'

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        ip = self.request.META.get('REMOTE_ADDR')
        # دریافت جزئیات و ثبت غیرهمزمان بازدید
        return BusinessService.get_business_detail(slug_or_id=slug, request_ip=ip)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # دریافت کسب‌وکارهای مرتبط
        context['related_businesses'] = BusinessService.get_related_businesses(self.object)
        return context
class BusinessViewSet(viewsets.ModelViewSet):
    queryset = Business.objects.filter(is_active=True)
    serializer_class = BusinessDetailSerializer

    def create(self, request, *args, **kwargs):
        serializer = BusinessCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # فراخوانی لایه سرویس به جای نوشتن مستقیم در View
        business = BusinessService.create_business(
            owner=request.user,
            **serializer.validated_data
        )

        output_serializer = BusinessDetailSerializer(business)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)