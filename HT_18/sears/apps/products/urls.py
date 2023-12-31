from django.urls import path

from apps.products.views import add_products
from apps.products.views import ProductDetailView
from apps.products.views import ProductListView
from apps.products.views import task

app_name = 'products'

urlpatterns = [
    path('products/', ProductListView.as_view(), name='my_products'),
    path('products/add-products/', add_products, name='add_products'),
    path('products/detail-product/<str:product_id>', ProductDetailView.as_view(), name='detail_product'),
    path('task/', task, name='task'),
]
