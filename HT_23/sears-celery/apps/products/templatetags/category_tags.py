from django import template
from django.db.models import Count
from django.utils.http import urlencode

from apps.products.models import Category

register = template.Library()


@register.simple_tag()
def show_categories():
    return (Category.objects
            .annotate(total_products_count=Count('products'))
            .filter(total_products_count__gte=5)
            .order_by('-total_products_count')
            )


@register.simple_tag(takes_context=True)
def change_params(context, **kwargs):
    query = context['request'].GET.dict()
    query.update(kwargs)
    return urlencode(query)
