from decimal import Decimal

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Sale(models.Model):
    class PaymentMethod(models.TextChoices):
        CASH = 'cash', 'Cash'
        ESEWA = 'esewa', 'eSewa'
        FONEPAY = 'fonepay', 'Fonepay'
        CARD = 'card', 'Card'
        BANK_TRANSFER = 'bank_transfer', 'Bank Transfer'
        OTHER = 'other', 'Other'

    invoice_number = models.CharField(max_length=32, unique=True, editable=False)
    customer_name = models.CharField(max_length=150, blank=True)
    customer_phone = models.CharField(max_length=20, blank=True)
    payment_method = models.CharField(max_length=20, choices=PaymentMethod.choices, default=PaymentMethod.CASH)
    sold_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    sold_at = models.DateTimeField(default=timezone.now)
    note = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['-sold_at']

    def __str__(self):
        return self.invoice_number

    def get_absolute_url(self):
        return reverse('sales:receipt', args=[self.pk])

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            self.invoice_number = self._generate_invoice_number()
        super().save(*args, **kwargs)

    @staticmethod
    def _generate_invoice_number():
        today = timezone.now().strftime('%Y%m%d')
        last = Sale.objects.filter(invoice_number__startswith=f'INV-{today}').order_by('-invoice_number').first()
        seq = int(last.invoice_number.split('-')[-1]) + 1 if last else 1
        return f'INV-{today}-{seq:04d}'

    @property
    def total_amount(self):
        return sum((item.line_total for item in self.items.all()), Decimal('0'))

    @property
    def total_cost(self):
        return sum((item.line_cost for item in self.items.all()), Decimal('0'))

    @property
    def profit(self):
        return self.total_amount - self.total_cost


class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('products.Product', on_delete=models.PROTECT, related_name='sale_items')
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, help_text='Selling price at time of sale')
    unit_cost = models.DecimalField(max_digits=12, decimal_places=2, help_text='Cost price at time of sale')

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'{self.product.name} x{self.quantity}'

    @property
    def line_total(self):
        return self.unit_price * self.quantity

    @property
    def line_cost(self):
        return self.unit_cost * self.quantity


class OnlineOrder(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending Dispatch'
        CONFIRMED = 'confirmed', 'Confirmed'
        DISPATCHED = 'dispatched', 'Out for Delivery'
        DELIVERED = 'delivered', 'Delivered'
        CANCELLED = 'cancelled', 'Cancelled'

    order_number = models.CharField(max_length=32, unique=True)
    customer_name = models.CharField(max_length=150)
    customer_phone = models.CharField(max_length=30)
    delivery_address = models.TextField()
    payment_method = models.CharField(max_length=50, default='Cash on Delivery (COD)')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0'))
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True, default='')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.order_number} - {self.customer_name}'


class OnlineOrderItem(models.Model):
    order = models.ForeignKey(OnlineOrder, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('products.Product', on_delete=models.SET_NULL, null=True, blank=True)
    product_name = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)

    @property
    def line_total(self):
        return self.unit_price * self.quantity

    def __str__(self):
        return f'{self.product_name} x{self.quantity}'

