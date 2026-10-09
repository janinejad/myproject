from django.contrib import admin
# from import_export.admin import ImportExportModelAdmin
from apps.categories.models import Category


# Register your models here.
@admin.register(Category)
class ProvinceAdmin(admin.ModelAdmin):
    class Meta:
        model = Category