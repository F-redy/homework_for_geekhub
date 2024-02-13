from apps.carts.api.serializers import CartSerializer
from apps.carts.models import Cart
from rest_framework.viewsets import ModelViewSet


class CartViewSet(ModelViewSet):
    queryset = Cart.objects.select_related('user', 'product')
    serializer_class = CartSerializer

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
