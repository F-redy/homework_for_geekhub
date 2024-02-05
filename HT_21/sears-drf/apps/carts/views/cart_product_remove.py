from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _

from apps.carts.utils import get_completed_cart_page
from apps.carts.utils import get_user_carts

SUCCESSES_DELETE_CART_MESSAGE = 'The product was successfully removed from the cart.'


@login_required
def cart_remove(request, cart_id):
    if request.method == 'DELETE':

        user_carts = get_user_carts(request)
        if user_carts.exists():
            cart = user_carts.filter(pk=cart_id).first()
            cart.delete()
            response_data = {
                'notification': _(SUCCESSES_DELETE_CART_MESSAGE),
                'success': True,
                'cart_items_html': get_completed_cart_page(request, user_carts),
            }

            return JsonResponse(response_data)
    return redirect('products:my_products')
