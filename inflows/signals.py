from django.db.models.signals import post_save
from django.dispatch import receiver
from inflows.models import Inflow


@receiver(signal=post_save, sender=Inflow)
def update_product_quantity(sender, instance, created, **kwargs):
    if created:
        if instance.quantity > 0:
            product = instance.product
            product.quantity += instance.quantity
            print(">>>", product, product.quantity)
            product.save()
