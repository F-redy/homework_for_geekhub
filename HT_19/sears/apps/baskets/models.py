from apps.products.models import Product
from django.db import models


class Basket(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.product_id

    def price(self):
        return round(self.product.final_price * self.quantity, 2)
