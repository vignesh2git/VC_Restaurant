from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Dish(models.Model):
    class Category(models.TextChoices):
        BEVERAGES = 'beverages', _('Coffee/Tea')
        SNACKS = 'snacks', _('Snacks')
        MEALS = 'meals', _('Meals')
        DESSERTS = 'desserts', _('Desserts')

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=4.5)
    is_promo = models.BooleanField(default=False)
    is_best_seller = models.BooleanField(default=False)
    is_new = models.BooleanField(default=False)
    category = models.CharField(max_length=20, choices=Category.choices, default=Category.MEALS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name


class Order(models.Model):
    class Status(models.TextChoices):
        CREATED = 'created', _('Created')
        PAID = 'paid', _('Paid')
        DELIVERED = 'delivered', _('Delivered')

    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    # Sequential order number per user (starts at 1). Not globally unique.
    user_order_no = models.PositiveIntegerField(default=0, help_text="Sequential number per user")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.CREATED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    delivery_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    delivery_pincode = models.CharField(max_length=10, blank=True)

    def total_price(self):
        items_total = sum(item.subtotal() for item in self.items.all())
        return items_total + (self.delivery_fee or 0)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)

    def subtotal(self):
        return self.quantity * self.unit_price


class DeliveryZone(models.Model):
    pincode_prefix = models.CharField(max_length=6, help_text="First 3-6 digits of PIN")
    fee = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    eta_min = models.PositiveIntegerField(default=30)
    eta_max = models.PositiveIntegerField(default=45)

    def __str__(self) -> str:
        return f"{self.pincode_prefix}: ₹{self.fee} ({self.eta_min}-{self.eta_max} mins)"


