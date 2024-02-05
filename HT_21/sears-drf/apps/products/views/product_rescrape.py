import sys
from subprocess import Popen

from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from apps.products.views import ACCESS_DENIED_MESSAGE

RESCRAPE_STARTED_MESSAGE = 'Re-scraping started. Please wait...'
SCRAPE_ERROR_MESSAGE = 'Oops... Scrape Process Failed'


def update_product(request, product_id):
    if not request.user.is_superuser:
        messages.error(request, _(ACCESS_DENIED_MESSAGE))
        return redirect('products:my_products')
    try:
        Popen([sys.executable, 'services/products/subscraper.py', product_id])
        messages.success(request, _(RESCRAPE_STARTED_MESSAGE))
    except Exception:
        messages.error(request, _(SCRAPE_ERROR_MESSAGE))

    return redirect(reverse('products:detail_product', kwargs={'product_id': product_id}))
