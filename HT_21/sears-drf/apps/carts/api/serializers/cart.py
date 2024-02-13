from apps.carts.models import Cart
from rest_framework import serializers


class CartSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    price = serializers.FloatField(
        read_only=True,
        source='product.final_price')
    quantity = serializers.IntegerField(required=True)
    products_price = serializers.FloatField(read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'price', 'quantity', 'product', 'products_price']
        read_only_fields = ['id', 'user', 'price', 'products_price']

    @staticmethod
    def get_products_price(obj):
        return obj.products_price()

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user

        return super().create(validated_data)
