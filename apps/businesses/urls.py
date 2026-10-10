from django.urls import path
from apps.businesses.views import HomeView, BusinessDetailView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('businesses/<str:slug>/', BusinessDetailView.as_view(), name='business_detail'),
]