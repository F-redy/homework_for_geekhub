from django.urls import path

from apps.products.api.views import CategoryListView
from apps.products.api.views import ProductList
from apps.products.api.views import ScrapeProduct

app_name = 'api_products'

urlpatterns = [
    path('products/', ProductList.as_view(), name='products_list'),
    path('scrape-products/', ScrapeProduct.as_view(), name='scrape_product'),
    path('categories/', CategoryListView.as_view(), name='categories_list'),
]
