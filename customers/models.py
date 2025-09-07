from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


# getting user model object
User = get_user_model()


class CustomerProfile(models.Model):
    """

    """
    USER_GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    account = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile')
    profile_avatar = models.ImageField(_('profile avatar'), upload_to='customer/profile_pics')
    gender = models.CharField(_('Gender'),max_length=5, choices=USER_GENDER_CHOICES, blank=True, null=True)
    # city = models.CharField(_('City'),max_length=50, blank=True, null=True)
    # address = models.CharField(_('address'), max_length=250, blank=True, null=True
    # post_code = models.CharField(_('Post Code'), max_length=10, blank=False, null=False)
    national_code = models.CharField(_('National Code'),max_length=10, unique=True, blank=True, null=True)
    id_card_picture = models.ImageField(_('ID card picture'), upload_to='customer/id_card_pics')
    is_verified = models.BooleanField(_('Is verified'), default=False)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)

    class Meta:
        ordering = ['-created_at']