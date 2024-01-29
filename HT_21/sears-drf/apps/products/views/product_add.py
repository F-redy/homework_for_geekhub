import sys
from subprocess import Popen

from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView

from apps.products.forms import AddProductForm
from apps.products.views import ACCESS_IS_DENIED

SUCCESS_MESSAGE_FORM = _('Data processing. It can take some time...')
ERROR_MESSAGE_FORM = _('Error: Scraping Process Invalid')


class AddProductsFormView(PermissionRequiredMixin, FormView):
    template_name = 'products/add_product.html'
    form_class = AddProductForm
    success_url = reverse_lazy('products:add_products')
    permission_denied_message = ACCESS_IS_DENIED
    permission_required = 'products.add_products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Add Products')
        return context

    def form_valid(self, form):
        product_ids = form.cleaned_data['user_input']
        try:
            Popen([sys.executable, 'services/products/subscraper.py', product_ids])
            messages.success(self.request, SUCCESS_MESSAGE_FORM)
        except Exception:
            messages.error(self.request, ERROR_MESSAGE_FORM)

        return super(AddProductsFormView, self).form_valid(form)

    def handle_no_permission(self):
        if self.request.user.is_anonymous:
            return redirect('users:login')
        messages.error(self.request, self.permission_denied_message)
        return redirect('products:my_products')
