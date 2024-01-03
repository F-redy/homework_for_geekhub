import sys
from subprocess import Popen

from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic import FormView
from django.views.generic import ListView

from apps.products.forms import AddProductForm
from apps.products.models import Product


class ProductListView(ListView):
    model = Product
    template_name = 'products/products.html'
    context_object_name = 'products_list'
    ordering = ['-created_at']
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'My Products'
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/detail_product.html'
    slug_url_kwarg = 'product_id'

    def get_object(self, queryset=None):
        return get_object_or_404(Product, product_id=self.kwargs['product_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Product - {self.object.name}'
        return context


class AddProductsFormView(FormView):
    template_name = 'products/add_product.html'
    form_class = AddProductForm
    success_url = reverse_lazy('products:my_products')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add Products'
        return context

    def form_valid(self, form):
        product_ids = form.cleaned_data['user_input']
        try:
            Popen([sys.executable, 'services/scraper/subscraper.py', product_ids])
            messages.success(self.request, 'Data processing. It can take some time...')
        except Exception:
            messages.error(self.request, 'Error: Scraping Process Invalid')

        return super(AddProductsFormView, self).form_valid(form)


def task(request):
    return render(request, 'products/task.html', {'title': 'Task'})
