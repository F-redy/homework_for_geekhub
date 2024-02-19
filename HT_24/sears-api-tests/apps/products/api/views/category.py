from django.db.models import Count
from rest_framework import generics
from rest_framework.permissions import AllowAny

from apps.products.api.serializers.category import CategorySerializer
from apps.products.models import Category


class CategoryListView(generics.ListAPIView):
    queryset = (
        Category.objects
        .annotate(quantity_products=Count('products'))
        .order_by('id')
    )
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
