from rest_framework import generics
from rest_framework.permissions import AllowAny

from apps.products.api.serializers.product import ProductSerializer
from apps.products.models import Product


class ProductList(generics.ListAPIView):
    queryset = Product.objects.all().select_related('category')
    serializer_class = ProductSerializer
    permission_classes = [AllowAny, ]
