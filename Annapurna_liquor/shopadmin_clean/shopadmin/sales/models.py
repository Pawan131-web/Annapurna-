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


import re
from urllib.parse import quote


class OnlineOrder(models.Model):
    class Status(models.TextChoices):
        NEW = 'new', 'New'
        CONTACTED = 'contacted', 'Contacted'
        COMPLETED = 'completed', 'Completed'
        CANCELLED = 'cancelled', 'Cancelled'

    order_number = models.CharField(max_length=64, unique=True)
    customer_name = models.CharField(max_length=150)
    customer_phone = models.CharField(max_length=30)
    customer_email = models.CharField(max_length=150, blank=True, default='')
    delivery_address = models.TextField(blank=True, default='')
    payment_method = models.CharField(max_length=50, default='WhatsApp Order / Direct')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0'))
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True, default='')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.order_number} - {self.customer_name}'

    @property
    def total_quantity(self):
        return sum((item.quantity for item in self.items.all()), 0)

    def get_status_badge_class(self):
        mapping = {
            self.Status.NEW: 'pill pill-brand',
            self.Status.CONTACTED: 'pill pill-warn',
            self.Status.COMPLETED: 'pill pill-success',
            self.Status.CANCELLED: 'pill pill-danger',
        }
        return mapping.get(self.status, 'pill pill-muted')

    def get_clean_phone(self):
        digits = re.sub(r'[^0-9]', '', self.customer_phone or '')
        if len(digits) == 10 and digits.startswith('9'):
            return f'977{digits}'
        return digits

    def get_whatsapp_url(self):
        clean_num = self.get_clean_phone()
        if not clean_num:
            return '#'
        msg = f"Hello {self.customer_name}! This is Annapurna Store following up on your order request ({self.order_number})."
        return f"https://wa.me/{clean_num}?text={quote(msg)}"


class OnlineOrderItem(models.Model):
    order = models.ForeignKey(OnlineOrder, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('products.Product', on_delete=models.SET_NULL, null=True, blank=True)
    product_name = models.CharField(max_length=200)
    product_image = models.CharField(max_length=500, blank=True, default='')
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0'))

    @property
    def line_total(self):
        return self.unit_price * self.quantity

    def get_image_url(self):
        if self.product_image:
            return self.product_image
        if self.product and self.product.primary_image:
            return self.product.primary_image.url
        return '/static/img/no-image.png'

    def __str__(self):
        return f'{self.product_name} x{self.quantity}'


