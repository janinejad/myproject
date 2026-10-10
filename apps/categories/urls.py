from django.urls import path
from .views import CategoryDetailView

urlpatterns = [
    path('categories/<slug:slug>/', CategoryDetailView.as_view(), name='category_detail'),
]