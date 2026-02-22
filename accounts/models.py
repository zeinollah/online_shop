import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
from django.utils import timezone
from datetime import timedelta

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


class EmailVerificationToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='verification_token')
    token = models.UUIDField(_('Token'), default=uuid.uuid4,unique=True , editable=False)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    expires_at = models.DateTimeField(_('Expires at'), null=True, blank=True)
    is_used = models.BooleanField(_('Is used'), default=False)

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(days=1)
        super().save(*args, **kwargs)

    def is_valid(self):
        return not self.is_used and timezone.now() < self.expires_at

    def __str__(self):
        return str(f"Token for {self.user.email}")

    class Meta:
        ordering = ['-created_at']