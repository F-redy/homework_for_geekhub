from django.urls import include
from django.urls import path
from rest_framework import routers

from apps.products.api_views.category import CategoryViewSet
from apps.products.api_views.product import ProductViewSet

app_name = 'api_products'

router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'products', ProductViewSet, basename='products')

urlpatterns = [
    path('', include(router.urls)),
]
