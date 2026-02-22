from django.db import models
import uuid
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from sellers.models import Store
from django.contrib.auth import get_user_model
User = get_user_model()


class Product(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(_("Product name"), max_length=200, blank=True, null=True)
    slug = models.SlugField(_("Slug"), max_length=200, unique=True, blank=True, null=True)
    description = models.TextField(_("Description"), max_length=500, blank=True, null=True)
    price = models.DecimalField(_("Price"), max_digits=10, decimal_places=3, blank=True, null=True)
    category = models.CharField(_("Category"), max_length=50, blank=True, null=True)
    in_stock = models.BooleanField(_("In stock"), default=True)
    picture = models.ImageField(_('Product picture'), upload_to='products/pictures', max_length=4, blank=True, null=True)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    def save(self, *args, **kwargs):
        # Create Slug when seller upload product
        if not self.slug:
            self.slug = self.generate_unique_slug()
        else:
        # Update the slug if seller update the product name
            if self.id:
                old_product = Product.objects.filter(id=self.id).first()
                if old_product != old_product.name :
                    self.slug = self.generate_unique_slug()
        super().save(*args, **kwargs)


    def generate_unique_slug(self):
        """Generate a unique slug for product."""
        base_slug = slugify(self.name)
        store_name = self.store.store_name
        slug = f"{base_slug}-{store_name}"
        count = 1
        while Product.objects.filter(slug=slug).exclude(id=self.id).exists():
            slug = f"{base_slug}-{store_name}-{count}"
            count += 1
        return slug

    class Meta:
        ordering = ('created_at',)


    def __str__(self):
        return f"{self.name}"