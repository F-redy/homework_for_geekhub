from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.views.generic import UpdateView

from apps.products.models import Product
from apps.products.views import ACCESS_IS_DENIED

SUCCESS_MESSAGE_FORM = _('Product was success updated.')


class UpdateProductsView(PermissionRequiredMixin, UpdateView):
    model = Product
    template_name = 'products/update_product.html'
    fields = ['name', 'brand', 'category', 'base_price', 'final_price', 'savings_price', 'short_description']
    permission_denied_message = ACCESS_IS_DENIED
    permission_required = 'products.change_product'

    def get_object(self, queryset=None):
        return get_object_or_404(Product, product_id=self.kwargs['product_id'])

    def handle_no_permission(self):
        if self.request.user.is_anonymous:
            messages.error(self.request, self.permission_denied_message)
            return redirect('users:login')
        messages.error(self.request, self.permission_denied_message)
        return redirect('products:my_products')

    def form_valid(self, form):
        messages.success(self.request, SUCCESS_MESSAGE_FORM)
        return super(UpdateProductsView, self).form_valid(form)
