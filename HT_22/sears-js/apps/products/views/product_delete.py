from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import DeleteView

from apps.products.models import Product


class DeleteProductsView(PermissionRequiredMixin, DeleteView):
    model = Product
    message = _('Product was successfully deleted.')
    permission_required = 'products.delete_product'

    def get_success_url(self):
        messages.success(self.request, self.message)
        return reverse_lazy('products:my_products')

    def handle_no_permission(self):
        if self.request.user.is_anonymous:
            messages.error(self.request, self.permission_denied_message)
            return redirect('users:login')
        messages.error(self.request, self.permission_denied_message)
        return redirect('products:my_products')
