from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from customers.models import CustomerProfile
from sellers.models import SellerProfile
from products.models import Product
from orders.models import Order, OrderItem



User = get_user_model()


class BaseDiscount(models.Model):
    """
    Use BaseDiscount class to separate site discount and seller discount.
    """
    DISCOUNT_TYPE_CHOICES = (
        ('percentage', 'Percentage'),
        ('fixed_amount', 'Fixed Amount'),
    )
    SCOPE_TYPE_CHOICES = (
        ('all_customers_all_products', 'All Customers - All Products'),
        ('all_customers_specific_products', 'All Customers - Specific Products'),
        ('specific_customer_all_products', 'Specific Customer - All Products'),
        ('specific_customer_specific_products', 'Specific Customer - Specific Products'),
    )

    code = models.CharField(_("Code"), max_length=50, unique=True)
    name = models.CharField(_("Name"), max_length=50, null=True, blank=True)
    discount_type = models.CharField(_("Discount type"), max_length=50, choices=DISCOUNT_TYPE_CHOICES, default='percentage')
    scope_type = models.CharField(_("Scope type"), max_length=50, choices=SCOPE_TYPE_CHOICES)
    value = models.DecimalField(_("Value"), max_digits=10, decimal_places=2, null=True, blank=True)
    is_used = models.BooleanField(_("Is used"), default=False)
    used_at = models.DateTimeField(_('used at'), null=True, blank=True)
    start_date = models.DateField(_('start day'), null=True, blank=True)
    end_date = models.DateField(_('end day'), null=True, blank=True)
    is_active = models.BooleanField(_('is active'), default=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        # abstract = True
        ordering = ('-created_at',)

    def __str__(self):
        return f"{self.name} - {self.code}"



class SellerDiscount(BaseDiscount):
    seller = models.ForeignKey(SellerProfile, on_delete=models.CASCADE, related_name='seller_discounts')
    target_customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, related_name='seller_discounts', null=True, blank=True)
    target_product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='seller_discounts', null=True, blank=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f"{self.seller} - {self.name} - {self.code}"



class SiteDiscount(BaseDiscount):
    target_customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, related_name='site_discount', null=True, blank=True)
    target_product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='site_discount', null=True, blank=True)

    class Meta:
        ordering = ('-created_at',)



class DiscountUsage(models.Model):
    seller_discount = models.ForeignKey(SellerDiscount, on_delete=models.CASCADE, null=True, blank=True, related_name='usage_records')
    site_discount = models.ForeignKey(SiteDiscount, on_delete=models.CASCADE, null=True, blank=True, related_name='usage_records')
    discount_code = models.CharField(_("Discount code"), max_length=50)
    discount_type = models.CharField(_("Discount type"), max_length=50)
    discount_value = models.DecimalField(_("Discount value"), max_digits=10, decimal_places=2)
    customer = models.ForeignKey(CustomerProfile, on_delete = models.CASCADE, related_name='discount_usages', null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='discount_usages')
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name='discount_usages')
    discount_amount = models.DecimalField(_("Discount amount"), max_digits=10, decimal_places=2)
    used_at = models.DateTimeField(_('used at'), auto_now_add=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f"{self.discount_code} used by {self.customer.full_name} on {self.used_at.strftime('%Y-%m-%d')}"

    @property
    def discount_owner(self):
        return 'site discount' if self.site_discount else 'seller discount'