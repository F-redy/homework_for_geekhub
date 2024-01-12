from django.db import models
from django.urls import reverse


class Product(models.Model):
    product_id = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=200)
    category = models.CharField(max_length=200)
    image_url = models.CharField(max_length=300, blank=True)
    base_price = models.FloatField()
    final_price = models.FloatField()
    savings_price = models.FloatField(default=0.0)
    url = models.URLField(blank=True)
    short_description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.product_id}'

    def get_absolute_url(self):
        return reverse('products:detail_product', kwargs={'product_id': self.product_id})

    class Meta:
        app_label = 'products'
