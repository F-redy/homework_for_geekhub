from apps.common.models import TimestampMixin
from apps.products.models import Product
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

MIN_QUANTITY = 0
MAX_QUANTITY = 100
ERROR_QUANTITY_MESSAGE = f'The quantity must be between {MIN_QUANTITY} and {MAX_QUANTITY}.'


class Cart(TimestampMixin, models.Model):
    user = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name=_('user')
    )
    product = models.OneToOneField(
        to=Product,
        on_delete=models.CASCADE,
        unique=True,
        verbose_name=_('product')
    )
    quantity = models.PositiveSmallIntegerField(
        default=MIN_QUANTITY,
        validators=[
            MinValueValidator(MIN_QUANTITY, message=_(ERROR_QUANTITY_MESSAGE)),
            MaxValueValidator(MAX_QUANTITY, message=_(ERROR_QUANTITY_MESSAGE))
        ],
        verbose_name=_('quantity')
    )
    session_key = models.CharField(
        max_length=32,
        null=True,
        blank=True,
        verbose_name=_('session key')
    )

    def __str__(self):
        return f'{self.user} | {self.product} | {self.quantity}'

    def products_price(self):
        return round(float(self.product.final_price * self.quantity), 2)

    class Meta:
        db_table = 'cart'
