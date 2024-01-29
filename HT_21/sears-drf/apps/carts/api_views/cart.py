from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet

from apps.carts.models import Cart
from apps.carts.serializers import CartSerializer


class CartViewSet(ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user).select_related('user', 'product')
