from rest_framework import serializers
from apps.businesses.models import Business

class BusinessSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Business
        fields = [
            'id', 'title', 'slug', 'description', 'category', 'category_name',
            'address', 'phone', 'mobile', 'website', 'logo', 'cover_image',
            'views_count', 'status', 'created_at'
        ]
        read_only_fields = ['status', 'views_count']