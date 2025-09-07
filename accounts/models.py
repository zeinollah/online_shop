from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager


class User(AbstractUser):
    USER_ROLE_CHOICES =(
        ('customer', 'customer'),
        ('seller', 'seller'),
    )
    username = None
    email = models.EmailField(_('Email Address'), unique=True, blank=False, null=False)
    phone_number = models.CharField(_('Phone Number'), unique=True, max_length=11, blank=False, null=False)
    address = models.CharField(_('Address'), max_length=100, blank=False, null=False)
    city = models.CharField(_('City'), max_length=15, blank=False, null=False)
    user_roll = models.CharField(_('Role'),choices=USER_ROLE_CHOICES, max_length=10, blank=False, null=False)
    post_code = models.CharField(_('Post Code'), max_length=10, blank=False, null=False)
    birth_day = models.DateField(_('Birth Day'), blank=True, null=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name','user_roll']

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}" + f" Role: {self.user_roll}"

    class Meta:
        ordering = ['-created_at']