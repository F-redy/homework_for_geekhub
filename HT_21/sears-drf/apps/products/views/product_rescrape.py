import sys
from subprocess import Popen

from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from apps.products.views import ACCESS_IS_DENIED

SUCCESS_MESSAGE = _('Re-scraping started. Wait a couple of seconds...')
ERROR_MESSAGE = _('Oops...Scraping Process Invalid')


def update_product(request, product_id):
    if not request.user.is_superuser:
        messages.error(request, ACCESS_IS_DENIED)
        return redirect('products:my_products')
    try:
        Popen([sys.executable, 'services/products/subscraper.py', product_id])
        messages.success(request, SUCCESS_MESSAGE)
    except Exception:
        messages.error(request, ERROR_MESSAGE)

    return redirect(reverse('products:detail_product', kwargs={'product_id': product_id}))
