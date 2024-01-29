from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _


@login_required
def show_carts(request):
    context = {'title': _('Cart')}

    return render(request, 'cart/index.html', context=context)
