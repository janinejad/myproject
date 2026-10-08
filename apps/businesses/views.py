from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Business
from .serializers import BusinessCreateSerializer, BusinessDetailSerializer
from .services import BusinessService


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