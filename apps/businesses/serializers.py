from rest_framework import serializers
from .models import Business

class BusinessCreateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    category_id = serializers.IntegerField()
    description = serializers.CharField()
    address = serializers.CharField()
    phone = serializers.CharField(required=False, allow_blank=True)
    mobile = serializers.CharField(required=False, allow_blank=True)

class BusinessDetailSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Business
        fields = ['id', 'title', 'slug', 'category_name', 'description', 'address', 'phone', 'status', 'created_at']