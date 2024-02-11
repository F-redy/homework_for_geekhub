from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from apps.carts.utils import get_response_data


@login_required
def update_cart_quantity(request, product_id):
    action = request.POST.get('action')
    quantity = int(request.POST.get('quantity'))

    return JsonResponse(data=get_response_data(request, product_id, action, quantity))
