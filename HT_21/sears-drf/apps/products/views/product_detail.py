from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView

from apps.products.models import Product


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/detail_product.html'
    slug_url_kwarg = 'product_id'

    def get_object(self, queryset=None):
        return get_object_or_404(Product, product_id=self.kwargs['product_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _(f'Product - {self.object.name}')
        return context
