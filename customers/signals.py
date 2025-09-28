from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import CustomerProfile

User = get_user_model()

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        CustomerProfile.objects.create(account = instance)


@receiver(post_save, sender=CustomerProfile)
def save_profile(sender, instance, **kwargs):
    if hasattr(instance, 'customer_profile')and instance.user_role == 'customer':
        instance.customer_profile.save()