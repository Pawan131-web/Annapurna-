from django.conf import settings
from django.db import models
from django.utils import timezone


class StockMovement(models.Model):
    class Direction(models.TextChoices):
        IN = 'in', 'Stock In'
        OUT = 'out', 'Stock Out'

    class Reason(models.TextChoices):
        PURCHASE = 'purchase', 'Purchase'
        SALE = 'sale', 'Sale'
        DAMAGE = 'damage', 'Damage'
        RETURN = 'return', 'Return'
        ADJUSTMENT = 'adjustment', 'Adjustment'

    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='stock_movements')
    direction = models.CharField(max_length=3, choices=Direction.choices)
    reason = models.CharField(max_length=12, choices=Reason.choices)
    quantity = models.PositiveIntegerField()
    quantity_before = models.PositiveIntegerField()
    quantity_after = models.PositiveIntegerField()
    note = models.CharField(max_length=255, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        sign = '+' if self.direction == self.Direction.IN else '-'
        return f'{self.product.name} {sign}{self.quantity} ({self.get_reason_display()})'
