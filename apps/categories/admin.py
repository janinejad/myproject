from django.contrib import admin
from apps.categories.models import Category
from import_export.admin import ImportExportModelAdmin

# Register your models here.
@admin.register(Category)
class ProvinceAdmin(ImportExportModelAdmin):
    class Meta:
        model = Category