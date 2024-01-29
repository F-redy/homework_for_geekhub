from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.products.models import Product
from apps.products.serializers.product import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().select_related('category')
    serializer_class = ProductSerializer

    http_method_names = ['get', 'put', 'head', 'options', 'delete']

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user and request.user.is_staf