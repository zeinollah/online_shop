from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _



class Customer(AbstractUser):
    email = models.EmailField(_('email address'), unique=True, blank=False, null=False)
    phone_number = models.CharField(_('phone number'), unique=True ,max_length=11, blank=False, null=False)
    address = models.CharField(_('address'), max_length=100, blank=False, null=False)
    post_code = models.IntegerField(_('post code'), max_length=10, blank=False, null=False)
    birth_day = models.DateField(_('birth day'), blank=True, null=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    def __str__(self):
        return self.first_name + " " + self.last_name

    class Meta:
        ordering = ['-created_at']