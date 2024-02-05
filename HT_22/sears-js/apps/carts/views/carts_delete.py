from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _

from apps.carts.utils import get_completed_cart_page
from apps.carts.utils import get_user_carts

SUCCESS_CLEAR_CART_MESSAGE = 'Cart successfully cleared. Your shopping basket is now empty.'


@login_required
def delete_carts(request):
    if request.method == 'DELETE':
        user_carts = get_user_carts(request)

        if user_carts.exists():
            user_carts.delete()
            response_data = {
                'notification': _(SUCCESS_CLEAR_CART_MESSAGE),
                'success': True,
                'cart_items_html': get_completed_cart_page(request, user_carts),
            }
            return JsonResponse(response_data)

    return redirect('carts:show_carts')
