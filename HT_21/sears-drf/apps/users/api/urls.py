from django.urls import include
from django.urls import path
from rest_framework import routers

from apps.users.api_views import UserViewSet

app_name = 'api_users'

router = routers.SimpleRouter()
router.register('', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
