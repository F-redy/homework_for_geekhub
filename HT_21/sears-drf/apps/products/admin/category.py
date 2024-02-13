from apps.products.models import Category
from apps.products.models import Product
from django.contrib import admin
from django.db.models import Count
from django.utils.translation import gettext_lazy as _


class ProductInline(admin.TabularInline):
    model = Product
    extra = 0
    fields = ('product_id', 'name', 'brand')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fieldsets = [
        (_('Title'), {'fields': ['name', 'slug']}),
        (_('Date'), {'fields': ['created_at', 'updated_at']}),
    ]
    list_display = ('name', 'get_quantity_product', 'created_at', 'updated_at')
    inlines = [ProductInline]

    readonly_fields = ('created_at', 'updated_at')
    search_fields = ('name', 'slug')
    list_filter = ['created_at', 'updated_at']

    list_per_page = 20

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(product_count=Count('products')).order_by('-product_count')
        return queryset

    def get_quantity_product(self, obj):
        return obj.product_count

    get_quantity_product.allow_tags = True
    get_quantity_product.short_description = _('Quantity')
    get_quantity_product.admin_order_field = _('product_count')
