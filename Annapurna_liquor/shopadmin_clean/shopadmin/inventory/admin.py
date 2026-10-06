from django.contrib import admin
from .models import StockMovement


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ('product', 'direction', 'reason', 'quantity', 'quantity_after', 'created_by', 'created_at')
    list_filter = ('direction', 'reason')
    search_fields = ('product__name', 'product__sku')
