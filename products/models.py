from django.db import models
from django.utils.translation import gettext_lazy as _
from sellers.models import SellerProfile



class Product(models.Model):
    seller = models.ForeignKey(SellerProfile, on_delete=models.CASCADE, related_name='seller')
    name = models.CharField(_("Product name"), max_length=200, blank=True, null=True)
    slug = models.SlugField(_("Slug"), max_length=200, unique=True, blank=True, null=True)
    description = models.TextField(_("Description"), max_length=500, blank=True, null=True)
    price = models.DecimalField(_("Price"), max_digits=10, decimal_places=3, blank=True, null=True)
    category = models.CharField(_("Category"), max_length=50, blank=True, null=True)
    in_stock = models.BooleanField(_("In stock"), default=True)
    picture = models.ImageField(_('Product picture'), upload_to='products/pictures', max_length=4, blank=True, null=True)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)


    class Meta:
        ordering = ('created_at',)


    def __str__(self):
        return f"{self.name}"