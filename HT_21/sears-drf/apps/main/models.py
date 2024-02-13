from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import TimestampMixin


class Task(TimestampMixin, models.Model):
    title = models.CharField(
        _('title'),
        max_length=50
    )
    description = models.TextField(
        _('description'),
    )
    notes = models.TextField(
        _('notes'),
        blank=True,
        null=True
    )

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'task'
