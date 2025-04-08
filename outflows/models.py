from django.db import models
from products.models import Product

# Create your models here.


class Outflow(models.Model):
    product = models.ForeignKey(
        to=Product, on_delete=models.PROTECT, related_name="outflows"
    )
    quantity = models.IntegerField()
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return str(self.product)
