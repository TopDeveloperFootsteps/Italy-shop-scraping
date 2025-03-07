from rest_framework import viewsets
from myapp.models.product import ProductItem
from myapp.serializers.product import ProductSerializer
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.viewsets import ModelViewSet

class ProductViewSet(ModelViewSet):
    queryset = ProductItem.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [OrderingFilter, SearchFilter]
    search_fields = ['description']
    ordering_fields  = ['price']