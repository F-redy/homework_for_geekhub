from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.products.models import Product
from apps.products.serializers.category import CategorySerializer

ERROR_MESSAGE_PRICE = 'Price must be greater than or equal to 0'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        base_price = serializers.DecimalField(
            max_digits=10,
            decimal_places=2,
            validators=[MinValueValidator(0, message=_(ERROR_MESSAGE_PRICE))]
        )
        final_price = serializers.DecimalField(
            max_digits=10,
            decimal_places=2,
            validators=[MinValueValidator(0, message=_(ERROR_MESSAGE_PRICE))]
        )
        savings_price = serializers.DecimalField(
            max_digits=10,
            decimal_places=2,
            validators=[MinValueValidator(0, message=_(ERROR_MESSAGE_PRICE))]
        )

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
