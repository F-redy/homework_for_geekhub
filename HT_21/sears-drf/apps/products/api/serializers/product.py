from rest_framework import serializers

from apps.products.models import Product


class ProductSerializer(serializers.ModelSerializer):
    base_price = serializers.FloatField()
    final_price = serializers.FloatField()
    savings_price = serializers.FloatField()

    class Meta:
        model = Product
        fields = (
            'pk',
            'product_id',
            'name',
            'brand',
            'base_price',
            'final_price',
            'savings_price',
            'url',
            'image_url',
            'short_description',
            'category',
        )
        read_only_fields = (
            'pk',
            'product_id',
            'name',
            'brand',
            'base_price',
            'final_price',
            'savings_price',
            'url',
            'image_url',
            'short_description',
            'category',
        )
