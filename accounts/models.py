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
    user_role = models.CharField(_('Role'),choices=USER_ROLE_CHOICES, max_length=10, blank=False, null=False)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name','user_role']

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}" + f" Role: {self.user_role}"

    class Meta:
        ordering = ['-created_at']