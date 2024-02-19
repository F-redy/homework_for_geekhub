from rest_framework import serializers

from apps.products.models import Category


class CategorySerializer(serializers.ModelSerializer):
    quantity_products = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = ('pk', 'name', 'quantity_products')
