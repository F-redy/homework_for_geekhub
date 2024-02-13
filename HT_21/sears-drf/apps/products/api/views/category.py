from apps.products.api.serializers.category import CategorySerializer
from apps.products.models import Category
from django.db.models import Count
from rest_framework import generics
from rest_framework.permissions import AllowAny


class CategoryListView(generics.ListAPIView):
    queryset = (
        Category.objects
        .annotate(quantity_products=Count('products'))
        .filter(quantity_products__gt=5).order_by('id')
    )
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
