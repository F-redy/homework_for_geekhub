from apps.carts import views
from django.urls import path

app_name = 'carts'

urlpatterns = [
    path('', views.show_carts, name='show_carts'),
    path('add-to-cart/<int:product_id>/', views.add_product_to_cart, name='cart_add'),
    path('update/<int:product_id>/', views.update_cart_quantity, name='cart_update'),
    path('cart-remove/<int:cart_id>/', views.cart_remove, name='cart_remove'),

    path('cart-clear/', views.delete_carts, name='cart_clear'),
]
