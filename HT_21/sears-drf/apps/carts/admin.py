from django.contrib import admin

from apps.carts.models import Cart


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'quantity')
    readonly_fields = ('id',)
    list_display_links = ('id', 'user')
