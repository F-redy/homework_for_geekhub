from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect

from apps.carts.common.messages import ERROR_MESSAGE
from apps.carts.common.messages import SUCCESS_MESSAGE
from apps.carts.models import Cart
from apps.products.models import Product


@login_required
def cart_product_sub(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    carts = Cart.objects.filter(user=request.user, product=product).select_related('user', 'product')
    if carts.exists():
        cart = carts.first()
        if cart.quantity > 1:
            cart.quantity -= 1
            cart.save()
            messages.success(request, SUCCESS_MESSAGE)
        else:
            messages.error(request, ERROR_MESSAGE)
    return redirect(request.META.get('HTTP_REFERER'))
