import sys
from subprocess import Popen

from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic import DetailView
from django.views.generic import ListView

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


def add_products(request):
    if request.method == 'POST':
        product_ids = request.POST.get('product-ids')

        try:
            Popen([sys.executable, 'services/scraper/subscraper.py', product_ids])
            messages.success(request, 'Data processing. It can take some time...')

        except Exception:
            messages.error(request, 'Error: Scraping Process Invalid')

        return redirect('products:my_products')

    else:
        context = {
            'placeholder': 'Enter ID separated by new line(example):'
                           '\np-00935112000P\np-A075482002\np-00937537000P\np-A119540351'
                           '\np-0000000000000000697300000000000007464308P'
                           '\np-A116635279\np-SPM10450584608\np-A085642481'
                           '\np-00602692000P\np-A011991588\np-A119988757',
            'title': 'Add Product'
        }

        return render(request, 'products/add_product.html', context=context)


def task(request):
    return render(request, 'products/task.html', {'title': 'Task'})
