from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _

from apps.carts.models import Cart


@login_required
def delete_carts(request, user_id):
    carts = Cart.objects.filter(user__id=user_id)

    if carts.exists():
        carts.delete()
        messages.success(request, _('Cart was cleared!'))

    return redirect(request.META.get('HTTP_REFERER'))
