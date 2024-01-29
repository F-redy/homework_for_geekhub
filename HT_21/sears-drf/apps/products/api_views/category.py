from django.db.models import Count
from rest_framework import viewsets

from apps.common.permission_classes import IsAdminOrReadOnly
from apps.products.models import Category
from apps.products.serializers.category import CategorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = (
        Category.objects
        .annotate(quantity_products=Count('products'))
        .filter(quantity_products__gt=5).order_by('id')
    )
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    http_method_names = ['get', 'head', 'options', 'delete']
