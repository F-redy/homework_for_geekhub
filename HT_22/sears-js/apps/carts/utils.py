from apps.carts.models import Cart
from apps.carts.models import ERROR_QUANTITY_MESSAGE
from apps.products.models import Product
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

SUCCESS_UPDATE_QUANTITY_MESSAGE = 'Product quantity successfully {} in the cart.'


def get_user_carts(request) -> QuerySet[Cart]:
    if request.user.is_authenticated:
        return Cart.objects.filter(user=request.user).select_related('product', 'user')


def get_total_quantity_cart_products(user_carts: QuerySet[Cart]) -> int:
    return sum(cart.quantity for cart in user_carts)


def get_total_price_cart_products(user_carts: QuerySet[Cart]) -> float:
    return round(sum(cart.quantity * cart.product.final_price for cart in user_carts), 2)


def get_completed_cart_page(request, user_carts: QuerySet[Cart]) -> str:
    cart_items_html = render_to_string(
        "cart/included/cart.html",
        {
            "carts": user_carts,
            'title': _('Cart'),
            'total_quantity': get_total_quantity_cart_products(user_carts),
            'total_price': get_total_price_cart_products(user_carts),
        },
        request=request
    )

    return cart_items_html


def update_cart_quantity(cart, action: str, quantity: int, success: bool = True):
    match action:
        case 'sub' if cart.quantity > 0:
            cart.quantity -= 1
            cart.save(update_fields=('quantity', 'updated_at'))
            notification = _(SUCCESS_UPDATE_QUANTITY_MESSAGE.format('decreased'))
        case 'add' if cart.quantity < 100:
            cart.quantity += 1
            cart.save(update_fields=('quantity', 'updated_at'))
            notification = _(SUCCESS_UPDATE_QUANTITY_MESSAGE.format('increased'))
        case 'update' if -1 < quantity < 101:
            cart.quantity = quantity
            cart.save(update_fields=('quantity', 'updated_at'))
            notification = _(SUCCESS_UPDATE_QUANTITY_MESSAGE.format('updated'))
        case _:
            success = False
            notification = _(ERROR_QUANTITY_MESSAGE)

    return success, notification


def get_response_data(request, product_id, action, quantity: int = None) -> dict:
    user_carts = get_user_carts(request)
    if user_carts.exists():
        product = get_object_or_404(Product, pk=product_id)
        cart = user_carts.filter(product=product).first()

        success, notification = update_cart_quantity(cart, action, quantity)
        return {
            'success': success,
            'notification': notification,
            'cart_items_html': get_completed_cart_page(request, user_carts)
        }
