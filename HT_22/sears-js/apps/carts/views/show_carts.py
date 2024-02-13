from apps.carts.utils import get_total_price_cart_products
from apps.carts.utils import get_total_quantity_cart_products
from apps.carts.utils import get_user_carts
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _


@login_required
def show_carts(request):
    user_carts = get_user_carts(request)

    context = {
        'title': _('Cart'),
        'carts': user_carts,
        'total_quantity': get_total_quantity_cart_products(user_carts),
        'total_price': get_total_price_cart_products(user_carts)
    }

    return render(request, 'cart/index.html', context=context)
