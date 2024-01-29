from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.carts.models import Cart
from apps.carts.serializers import CartSerializer


class CartViewSet(ModelViewSet):
    serializer_class = CartSerializer

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user).select_related('user', 'product')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.validated_data['user'] = self.request.user
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


