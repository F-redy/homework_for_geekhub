from apps.products.models import Product
from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fieldsets = [
        (_('Date information'), {'fields': ['created_at', 'updated_at'], 'classes': ['collapse']}),
        (_('Product Information'), {'fields': ['name', 'product_id', 'brand', 'category'], 'classes': ['collapse']}),
        (_('Price'), {'fields': ['base_price', 'final_price', 'savings_price'], 'classes': ['collapse']}),
        (_('URL'), {'fields': ['url', 'image_url'], 'classes': ['collapse']}),
        (_('Description'), {'fields': ['short_description'], 'classes': ['collapse']})
    ]

    list_display = ('product_id', 'final_price', 'created_at', 'updated_at', 'view_product_url')
    readonly_fields = ('created_at', 'updated_at')
    search_fields = ('product_id',)
    list_filter = ['created_at', 'updated_at']
    list_per_page = 20

    def view_product_url(self, obj):
        return format_html(f'<a href="{obj.get_absolute_url()}" target="_blank">view on site</a>')

    view_product_url.allow_tags = True
    view_product_url.short_description = _('View Product')
