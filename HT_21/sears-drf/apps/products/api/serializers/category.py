from apps.products.models import Category
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    quantity_products = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'quantity_products')
