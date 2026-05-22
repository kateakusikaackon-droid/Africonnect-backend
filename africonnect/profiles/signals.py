from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import SupplierProfile

User = settings.AUTH_USER_MODEL


@receiver(post_save, sender=User)
def create_supplier_profile(sender, instance, created, **kwargs):
    if created:
        SupplierProfile.objects.create(user=instance)