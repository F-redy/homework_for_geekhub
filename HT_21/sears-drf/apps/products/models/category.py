from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from apps.common.models import TimestampMixin


class Category(TimestampMixin, models.Model):
    name = models.CharField(_('name'), max_length=200)
    slug = models.SlugField(_('slug'), max_length=250)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:by_category', kwargs={'cat_slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(str(self.name))
        return super(Category, self).save(*args, **kwargs)

    class Meta:
        db_table = 'category'
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
