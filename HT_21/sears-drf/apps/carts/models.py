from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import F
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _

from apps.common.models import TimestampMixin
from apps.products.models import Product


# class CartQuerySet(models.QuerySet):
#     def total_price(self):
#         return sum(cart.get_total_price() for cart in self)
#
#     def total_quantity(self):
#         return sum(cart.quantity for cart in self) if self else 0
class CartQuerySet(models.QuerySet):
    def total_price(self):
        return self.aggregate(total_price=Sum(F('product__final_price') * F('quantity')))['total_price'] or 0

    def total_quantity(self):
        return self.aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0


class Cart(TimestampMixin, models.Model):
    user = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name=_('user')
    )
    product = models.ForeignKey(
        to=Product,
        on_delete=models.CASCADE,
        verbose_name=_('product')
    )
    quantity = models.PositiveSmallIntegerField(
        default=0,
        verbose_name=_('quantity')
    )
    session_key = models.CharField(
        max_length=32,
        null=True,
        blank=True,
        verbose_name=_('session key')
    )

    objects = CartQuerySet.as_manager()

    def __str__(self):
        return f'{self.user.username} | {self.product.name} | {self.quantity}'

    def products_price(self):
        return round(float(self.product.final_price * self.quantity), 2)

    class Meta:
        db_table = 'cart'
