from django.db.models.signals import post_save
from django.dispatch import receiver
from outflows.models import Outflow


@receiver(signal=post_save, sender=Outflow)
def update_product_quantity(sender, instance, created, **kwargs):
    if created:
        if instance.quantity > 0:
            product = instance.product
            if product.quantity >= instance.quantity:
                product.quantity -= instance.quantity
                product.save()
