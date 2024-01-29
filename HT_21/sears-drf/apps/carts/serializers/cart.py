from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.carts.models import Cart


class CartSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(
        read_only=True,
        source='product.final_price',
        max_digits=10,
        decimal_places=2
    )
    quantity = serializers.IntegerField(
        required=True,
        validators=[
            MinValueValidator(1, message=_('Quantity must be greater than or equal to 1')),
            MaxValueValidator(100, message=_('Quantity must be less than or equal to 100'))
        ]
    )
    products_price = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'price', 'quantity', 'product', 'products_price']
        read_only_fields = ['id', 'user', 'price', 'products_price']
        write_only_fields = ['product', ]

    def get_products_price(self, obj):
        return obj.products_price()
