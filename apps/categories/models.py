from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from apps.core.models import TimeStampedModel

class Category(MPTTModel, TimeStampedModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True, allow_unicode=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    icon = models.ImageField(upload_to='categories/icons/', null=True, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class MPTTMeta:
        order_insertion_by = ['order', 'name']

    def __str__(self):
        return self.name