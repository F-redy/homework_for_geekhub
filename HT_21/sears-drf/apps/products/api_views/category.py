from django.db.models import Count
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from apps.products.models import Category
from apps.products.serializers.category import CategorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = (
        Category.objects
        .annotate(quantity_products=Count('products'))
        .filter(quantity_products__gt=5).order_by('id')
    )
    serializer_class = CategorySerializer
    permission_classes = [AllowAny, ]
    http_method_names = ['get', ]
