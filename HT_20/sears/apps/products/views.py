import sys
from subprocess import Popen

from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Count
from django.shortcuts import get_list_or_404
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import FormView
from django.views.generic import ListView
from django.views.generic import UpdateView

from apps.products.forms import AddProductForm
from apps.products.models import Category
from apps.products.models import Product

ACCESS_IS_DENIED = 'Access Denied: You do not have permission to access this page.'


class CategoryListView(ListView):
    model = Category
    template_name = 'products/categories.html'
    context_object_name = 'list_categories'
    extra_context = {'title': 'Categories'}
    paginate_by = 20

    def get_queryset(self):
        return Category.objects.annotate(total_products=Count('products')).order_by('-total_products')


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
            context['title'] = f'Products By Category: {category.name}'
            context['category'] = category.name
        else:
            context.setdefault('title', 'My Products')

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


class AddProductsFormView(PermissionRequiredMixin, FormView):
    template_name = 'products/add_product.html'
    form_class = AddProductForm
    success_url = reverse_lazy('products:add_products')
    permission_denied_message = ACCESS_IS_DENIED
    permission_required = 'products.add_products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add Products'
        return context

    def form_valid(self, form):
        product_ids = form.cleaned_data['user_input']
        try:
            Popen([sys.executable, 'services/products/subscraper.py', product_ids])
            messages.success(self.request, 'Data processing. It can take some time...')
        except Exception:
            messages.error(self.request, 'Error: Scraping Process Invalid')

        return super(AddProductsFormView, self).form_valid(form)

    def handle_no_permission(self):
        if self.request.user.is_anonymous:
            return redirect('users:login')
        messages.error(self.request, self.permission_denied_message)
        return redirect('products:my_products')


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
        messages.success(self.request, 'Product was success updated.')
        return super(UpdateProductsView, self).form_valid(form)


class DeleteProductsView(PermissionRequiredMixin, DeleteView):
    model = Product
    message = 'Product was successfully deleted.'
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


def update_product(request, product_id):
    if not request.user.is_superuser:
        messages.error(request, ACCESS_IS_DENIED)
        return redirect('products:my_products')
    try:
        Popen([sys.executable, 'services/products/subscraper.py', product_id])
        messages.success(request, 'Re-scraping started. Wait a couple of seconds...')
    except Exception:
        messages.error(request, 'Oops...Scraping Process Invalid')

    return redirect(reverse('products:detail_product', kwargs={'product_id': product_id}))
