from django.urls import path

from apps.carts import views

app_name = 'carts'

urlpatterns = [
    path('', views.show_carts, name='show_carts'),
    path('cart-add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart-product-sub/<int:product_id>/', views.cart_product_sub, name='cart_product_sub'),
    path('cart-product-add/<int:product_id>/', views.cart_product_add, name='cart_product_add'),
    path('cart-update/<int:product_id>/', views.cart_update, name='cart_update'),
    path('cart-remove/<int:cart_id>/', views.cart_remove, name='cart_remove'),
    path('cart-delete-carts/<int:user_id>/', views.delete_carts, name='delete_carts'),
]
