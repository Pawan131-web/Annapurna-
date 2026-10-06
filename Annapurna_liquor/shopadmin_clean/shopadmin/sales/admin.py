from django.contrib import admin
from .models import Sale, SaleItem, OnlineOrder, OnlineOrderItem


class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 1


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'customer_name', 'payment_method', 'sold_by', 'sold_at')
    list_filter = ('payment_method', 'sold_at')
    search_fields = ('invoice_number', 'customer_name', 'customer_phone')
    inlines = [SaleItemInline]


class OnlineOrderItemInline(admin.TabularInline):
    model = OnlineOrderItem
    extra = 0


@admin.register(OnlineOrder)
class OnlineOrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'customer_name', 'customer_phone', 'status', 'total_amount', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('order_number', 'customer_name', 'customer_phone', 'delivery_address')
    list_editable = ('status',)
    inlines = [OnlineOrderItemInline]

