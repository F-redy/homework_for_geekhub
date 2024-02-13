from apps.baskets import views
from django.urls import path

app_name = 'baskets'

urlpatterns = [
    path('', views.show_basket, name='show'),
    path('add/<str:product_id>/', views.add_basket, name='add'),
    path('add-product/<str:product_id>/', views.add_product, name='add-product'),
    path('sub-product/<str:product_id>/', views.sub_product, name='sub-product'),
    path('change-product/<str:product_id>/', views.change_basket, name='change-basket'),
    path('remove/<str:product_id>/', views.remove_basket, name='remove'),
    path('clear/', views.clear_basket, name='clear_basket'),
]
