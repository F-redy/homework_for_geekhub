from django import template

# from apps.carts.models import Cart
from apps.carts.utils import get_user_carts

register = template.Library()


@register.simple_tag()
def user_carts(request):
    # if request.user.is_authenticated:
    #     return Cart.objects.filter(user=request.user).select_related('product', 'user')
    return get_user_carts(request)
