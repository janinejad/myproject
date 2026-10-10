from django.core.paginator import Paginator
from django.views.generic import DetailView
from apps.categories.models import Category
from apps.businesses.models import Business


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'categories/category_detail.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        businesses_qs = Business.objects.filter(category=self.object)

        # تنظیم تعداد کسب‌وکارها در هر صفحه روی 20 عدد
        paginator = Paginator(businesses_qs, 20)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['businesses'] = page_obj
        context['page_obj'] = page_obj
        context['is_paginated'] = page_obj.has_other_pages()
        return context