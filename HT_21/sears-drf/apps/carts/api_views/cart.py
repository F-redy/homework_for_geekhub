from rest_framework.viewsets import ModelViewSet

from apps.carts.models import Cart
from apps.carts.serializers.cart import CartSerializer


class CartViewSet(ModelViewSet):
    serializer_class = CartSerializer

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user).select_related('user')
