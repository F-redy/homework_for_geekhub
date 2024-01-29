from rest_framework import viewsets

from apps.common.permission_classes import IsAdminOrReadOnly
from apps.products.models import Product
from apps.products.serializers.product import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().select_related('category')
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly, ]

    http_method_names = ['get', 'head', 'options', 'delete']
