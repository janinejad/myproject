from datetime import datetime

from django.db import models
from django.utils import timezone
from imagekit.models import ProcessedImageField
from pilkit.processors import ResizeToFill

from extensions.utils import get_filename_ext


def upload_image_path(instance, filename):
    name, ext = get_filename_ext(filename)
    file_name = f"{timezone.now()}{ext}"
    return f"products/{datetime.today().year}/{datetime.today().month}/{file_name}"

class Category(models.Model):
    name = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(max_length=150, unique=True, allow_unicode=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    icon = models.CharField(max_length=100, blank=True, help_text="SVG or Icon Class")
    image = ProcessedImageField(upload_to=upload_image_path,format='WEBP', processors=[ResizeToFill(200, 200)],
                                verbose_name='تصویر شاخص',
                                blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name