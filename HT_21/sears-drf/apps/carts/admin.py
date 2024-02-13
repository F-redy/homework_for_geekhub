from apps.carts.models import Cart
from django.contrib import admin


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'quantity')
    readonly_fields = ('id',)
    list_display_links = ('id', 'user')
