from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class SellerProfile(models.Model):
    account = models.OneToOneField(User, on_delete=models.CASCADE, related_name='seller_profile')
    phone_number = models.CharField(_('Phone Number'), max_length=11, unique=True, blank=True, null=True)
    city = models.CharField(_('City'), max_length=50, blank=True, null=True)
    address = models.CharField(_('address'), max_length=250, blank=True, null=True)
    store_name = models.CharField(_('store name'), max_length=50, blank=True, null=True)
    physical_store = models.BooleanField(_('Physical Store'), default=True)
    store_address = models.CharField(_('store Address'), max_length=250, blank=True, null=True)
    post_code = models.CharField(_('Post Code'), max_length=10, blank=True, null=True)
    national_code = models.CharField(_('national Code'), max_length=10, unique=True, blank=True, null=True)
    id_card_picture = models.ImageField(_('ID card picture'), upload_to='customer/id_card_pics', blank=True, null=True)
    birth_day = models.DateField(_('Birth day'), blank=True, null=True)
    is_verified = models.BooleanField(_('Is verified'), default=False)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)

    @property
    def full_name(self):
        return f"{self.account.first_name} {self.account.last_name}"

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.full_name

    # TODO = Create store model and separate seller and store
    # TODO = Write @property for total in stock product for seller or store
    # TODO = Correct the path of id_card_picture to 'seller/id_card_pics'