from django.db.models import Count
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView

from apps.products.models import Category


class CategoryListView(ListView):
    model = Category
    template_name = 'products/categories.html'
    context_object_name = 'list_categories'
    extra_context = {'title': _('Categories')}
    paginate_by = 20

    def get_queryset(self):
        return Category.objects.annotate(total_products_count=Count('products')).order_by('-total_products_count')
