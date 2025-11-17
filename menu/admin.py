from django.contrib import admin
from .models import Dish, Order, OrderItem, DeliveryZone


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "category", "is_active")
    list_filter = ("is_active", "category", "is_promo", "is_best_seller", "is_new")
    search_fields = ("name", "description")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "status", "delivery_pincode", "delivery_fee", "created_at")
    list_filter = ("status", "created_at")
    inlines = [OrderItemInline]


@admin.register(DeliveryZone)
class DeliveryZoneAdmin(admin.ModelAdmin):
    list_display = ("pincode_prefix", "fee", "eta_min", "eta_max")
    search_fields = ("pincode_prefix",)


