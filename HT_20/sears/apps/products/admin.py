from apps.products.models import Category
from apps.products.models import Product
from django.contrib import admin
from django.db.models import Count
from django.utils.html import format_html


class ProductInline(admin.TabularInline):
    model = Product
    extra = 0
    fields = ('product_id', 'name', 'brand')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Title', {'fields': ['name', 'slug']}),
        ('Date', {'fields': ['created_at', 'updated_at']}),
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
    get_quantity_product.short_description = 'Quantity'
    get_quantity_product.admin_order_field = 'product_count'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Date information', {'fields': ['created_at', 'updated_at'], 'classes': ['collapse']}),
        ('Product Information', {'fields': ['name', 'product_id', 'brand', 'category'], 'classes': ['collapse']}),
        ('Price', {'fields': ['base_price', 'final_price', 'savings_price'], 'classes': ['collapse']}),
        ('URL', {'fields': ['url', 'image_url'], 'classes': ['collapse']}),
        ('Description', {'fields': ['short_description'], 'classes': ['collapse']})
    ]

    list_display = ('product_id', 'final_price', 'created_at', 'updated_at', 'view_product_url')
    readonly_fields = ('created_at', 'updated_at')
    search_fields = ('product_id',)
    list_filter = ['created_at', 'updated_at']
    list_per_page = 20

    def view_product_url(self, obj):
        return format_html(f'<a href="{obj.get_absolute_url()}" target="_blank">view on site</a>')

    view_product_url.allow_tags = True
    view_product_url.short_description = 'View Product'
