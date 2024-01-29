from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect

from apps.carts.common.messages import SUCCESS_MESSAGE
from apps.carts.models import Cart
from apps.products.models import Product


@login_required
def cart_add(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    carts = Cart.objects.filter(user=request.user, product=product).select_related('user', 'product')

    if carts.exists():
        cart = carts.first()
        cart.quantity += 1
        cart.save()

    else:
        Cart.objects.create(user=request.user, product=product, quantity=1)
    messages.success(request, SUCCESS_MESSAGE)

    return redirect(request.META.get('HTTP_REFERER'))
