from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from apps.common.models import TimestampMixin
from apps.products.models import Category

ERROR_PRICE_MESSAGE = 'Must be greater than or equal to {}.'
MIN_PRICE = 1.0
MIN_SAVINGS_PRICE = 0.0


class Product(TimestampMixin, models.Model):
    product_id = models.CharField(
        _('product_id'),
        max_length=75,
        unique=True
    )
    name = models.CharField(
        _('name'),
        max_length=200,
        default=_('No name provided'),
        blank=True
    )
    brand = models.CharField(
        _('brand'),
        max_length=100,
        default=_('No brand provided'),
        blank=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='products',
        null=True,
        default=_('No category provided'),
        verbose_name=_('category')
    )
    image_url = models.URLField(
        _('image_url'),
        default=_('No image provided'),
        blank=True
    )
    base_price = models.DecimalField(
        _('base_price'),
        max_digits=10,
        decimal_places=2,
        blank=True,
        default=MIN_PRICE,
        validators=[
            MinValueValidator(
                MIN_PRICE, message=_(ERROR_PRICE_MESSAGE.format(MIN_PRICE))
            )
        ]
    )
    final_price = models.DecimalField(
        _('final_price'),
        max_digits=10,
        decimal_places=2,
        blank=True,
        default=MIN_PRICE,
        validators=[
            MinValueValidator(
                MIN_PRICE, message=_(ERROR_PRICE_MESSAGE.format(MIN_PRICE))
            )
        ]
    )
    savings_price = models.DecimalField(
        _('savings_price'),
        max_digits=10,
        decimal_places=2,
        blank=True,
        default=MIN_SAVINGS_PRICE,
        validators=[
            MinValueValidator(
                MIN_SAVINGS_PRICE,
                message=_(ERROR_PRICE_MESSAGE.format(MIN_SAVINGS_PRICE))
            )
        ]
    )
    url = models.URLField(
        _('url'),
        blank=True,
        default=_('No url provided')
    )
    short_description = models.TextField(
        _('short_description'),
        blank=True,
        null=True
    )

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('products:detail_product', kwargs={'product_id': self.product_id})

    class Meta:
        db_table = 'product'
