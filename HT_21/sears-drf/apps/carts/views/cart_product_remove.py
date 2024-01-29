from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _

from apps.carts.models import Cart


@login_required
def cart_remove(request, cart_id):
    cart = get_object_or_404(Cart, pk=cart_id)
    if cart:
        product_id = cart.product.product_id
        cart.delete()
        messages.success(request, _(f'Deleted {product_id} from cart.'))

    return redirect(request.META.get('HTTP_REFERER'))
