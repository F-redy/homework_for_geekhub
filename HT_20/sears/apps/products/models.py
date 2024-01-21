from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:by_category', kwargs={'cat_slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(str(self.name))
        return super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Product(models.Model):
    product_id = models.CharField(max_length=75, unique=True)
    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    image_url = models.URLField(blank=True)
    base_price = models.FloatField()
    final_price = models.FloatField(default=0.0)
    savings_price = models.FloatField(default=0.0)
    url = models.URLField(blank=True)
    short_description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.product_id}'

    def get_absolute_url(self):
        return reverse('products:detail_product', kwargs={'product_id': self.product_id})
