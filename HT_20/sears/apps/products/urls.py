from apps.products import views
from django.urls import path

app_name = 'products'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='my_products'),

    path('add-products/', views.AddProductsFormView.as_view(), name='add_products'),
    path('detail-product/<str:product_id>/', views.ProductDetailView.as_view(), name='detail_product'),
    path('change-product/<str:product_id>/', views.UpdateProductsView.as_view(), name='change_product'),
    path('update-product/<str:product_id>/', views.update_product, name='update_product'),
    path('delete/<int:pk>/', views.DeleteProductsView.as_view(), name='delete_product'),

    path('category/', views.CategoryListView.as_view(), name='categories'),
    path('category/<slug:cat_slug>/', views.ProductListView.as_view(), name='by_category'),
]
