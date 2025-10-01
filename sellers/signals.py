from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import SellerProfile

User = get_user_model()

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created and instance.user_role== "seller":
        SellerProfile.objects.create(account=instance)

@receiver(post_save, sender=User)
def update_profile(sender, instance, **kwargs):
    if hasattr(instance, 'seller_profile') and instance.user_role == 'seller':
        instance.seller_profile.save()