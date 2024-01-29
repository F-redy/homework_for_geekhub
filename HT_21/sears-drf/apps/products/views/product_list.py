from django.shortcuts import get_list_or_404
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView

from apps.products.models import Category
from apps.products.models import Product


class ProductListView(ListView):
    model = Product
    template_name = 'products/products.html'
    context_object_name = 'products_list'
    paginate_by = 20

    def get_queryset(self):
        slug = self.kwargs.get('cat_slug')
        if slug:
            return get_list_or_404(Product, category__slug=slug)
        return Product.objects.order_by(self.get_ordering()).select_related('category')

    def get_ordering(self):
        return self.request.GET.get('ordering', '-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('cat_slug')
        if slug:
            category = get_object_or_404(Category, slug=slug)
            context['title'] = _(f'Products By Category: {category.name}')
            context['category'] = _(category.name)
        else:
            context.setdefault('title', _('My Products'))

        return context
