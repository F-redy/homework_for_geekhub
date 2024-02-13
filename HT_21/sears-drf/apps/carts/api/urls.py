from apps.carts.api.views import CartViewSet
from django.urls import include
from django.urls import path
from rest_framework import routers

app_name = 'api_carts'

router = routers.SimpleRouter()
router.register(r'', CartViewSet, basename='cart')

urlpatterns = [
    path('', include(router.urls)),
]
