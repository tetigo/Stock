from django.contrib import admin
from . import models


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "brand",
        "description",
        "serie_number",
        "cost_price",
        "selling_price",
        "quantity",
    )
    search_fields = ("title",)


admin.site.register(models.Product, ProductAdmin)
