"""
URL configuration for sears project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include
from django.urls import path
from drf_spectacular.views import SpectacularAPIView
from drf_spectacular.views import SpectacularRedocView
from drf_spectacular.views import SpectacularSwaggerView

from apps.main.views import page_not_found
from settings import main

api = [
    path('', include('apps.products.api_urls', namespace='api_products')),
    path('cart/', include('apps.carts.api_urls', namespace='api_carts')),

    path('users/', include('apps.users.api_urls', namespace='api_users')),
]

urlpatterns = [
    path('', include('apps.main.urls', namespace='main')),

    # ordinary
    path('products/', include('apps.products.urls', namespace='products')),
    path('carts/', include('apps.carts.urls', namespace='carts')),
    path('users/', include('apps.users.urls', namespace='users')),

    # api
    path('api/', include(api)),

    # Spectacular
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    path('admin/', admin.site.urls),
]

if main.DEBUG:
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]

handler404 = page_not_found
