from django.contrib import admin
from .models import PriceHistory, Product, ProductImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'department', 'brand', 'category', 'selling_price', 'quantity_in_stock', 'status', 'is_deleted')
    list_filter = ('department', 'category', 'brand', 'supplier', 'status', 'is_deleted')
    search_fields = ('name', 'sku', 'brand', 'tags')
    inlines = [ProductImageInline]


@admin.register(PriceHistory)
class PriceHistoryAdmin(admin.ModelAdmin):
    list_display = ('product', 'price_type', 'old_price', 'new_price', 'changed_by', 'changed_at')
    list_filter = ('price_type',)
