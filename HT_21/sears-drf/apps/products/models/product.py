from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from apps.common.models import TimestampMixin
from apps.products.models import Category


class Product(TimestampMixin, models.Model):
    product_id = models.CharField(_('product_id'), max_length=75, unique=True)
    name = models.CharField(_('name'), max_length=200)
    brand = models.CharField(_('brand'), max_length=100)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products',
        verbose_name=_('category')
    )
    image_url = models.URLField(_('image_url'), blank=True)
    base_price = models.FloatField(_('base_price'), )
    final_price = models.FloatField(_('final_price'), default=0.0)
    savings_price = models.FloatField(_('savings_price'), default=0.0)
    url = models.URLField(_('url'), blank=True)
    short_description = models.TextField(_('short_description'), )

    def __str__(self):
        return f'{self.product_id}'

    def get_absolute_url(self):
        return reverse('products:detail_product', kwargs={'product_id': self.product_id})

    class Meta:
        db_table = 'product'
