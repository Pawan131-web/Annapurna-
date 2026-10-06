from decimal import Decimal

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Product(models.Model):
    class Unit(models.TextChoices):
        PIECE = 'piece', 'Piece'
        KG = 'kg', 'Kilogram'
        GRAM = 'g', 'Gram'
        LITRE = 'l', 'Litre'
        BOX = 'box', 'Box'
        PACK = 'pack', 'Pack'
        DOZEN = 'dozen', 'Dozen'

    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        INACTIVE = 'inactive', 'Inactive'

    class Department(models.TextChoices):
        LIQUOR = 'liquor', 'Liquor'
        GROCERY = 'grocery', 'Grocery'
        BOTH = 'both', 'Both / General'

    name = models.CharField(max_length=200)
    sku = models.CharField('SKU / Code', max_length=64, unique=True, blank=True)
    category = models.ForeignKey('categories.Category', on_delete=models.PROTECT, related_name='products')
    supplier = models.ForeignKey('suppliers.Supplier', on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    department = models.CharField(max_length=20, choices=Department.choices, default=Department.LIQUOR)
    brand = models.CharField(max_length=120, blank=True, default='')
    volume = models.CharField(max_length=60, blank=True, default='', help_text='e.g. 750ML, 1L, 5KG')
    alcohol_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text='e.g. 40.0 for 40% ABV')
    origin = models.CharField(max_length=100, blank=True, default='', help_text='Country or Region of origin')
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=Decimal('5.0'))
    original_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, help_text='MRP before discount')
    tags = models.TextField(blank=True, default='', help_text='Comma-separated search tags')
    description = models.TextField(blank=True)
    cost_price = models.DecimalField(max_digits=12, decimal_places=2)
    selling_price = models.DecimalField(max_digits=12, decimal_places=2)
    quantity_in_stock = models.PositiveIntegerField(default=0)
    unit = models.CharField(max_length=10, choices=Unit.choices, default=Unit.PIECE)
    low_stock_threshold = models.PositiveIntegerField(default=10)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ACTIVE)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['sku']),
            models.Index(fields=['status']),
            models.Index(fields=['department']),
            models.Index(fields=['brand']),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.sku:
            import uuid
            self.sku = f'PRD-{uuid.uuid4().hex[:6].upper()}'
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('products:detail', args=[self.pk])

    @property
    def is_low_stock(self):
        return self.quantity_in_stock <= self.low_stock_threshold

    @property
    def profit_margin(self):
        if self.cost_price:
            return ((self.selling_price - self.cost_price) / self.cost_price) * Decimal('100')
        return Decimal('0')

    @property
    def primary_image(self):
        img = self.images.filter(is_primary=True).first()
        return img or self.images.first()


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/%Y/%m/')
    is_primary = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_primary', 'uploaded_at']

    def __str__(self):
        return f'Image for {self.product.name}'


class PriceHistory(models.Model):
    class PriceType(models.TextChoices):
        COST = 'cost', 'Cost price'
        SELLING = 'selling', 'Selling price'

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='price_history')
    price_type = models.CharField(max_length=10, choices=PriceType.choices)
    old_price = models.DecimalField(max_digits=12, decimal_places=2)
    new_price = models.DecimalField(max_digits=12, decimal_places=2)
    changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    changed_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-changed_at']
        verbose_name_plural = 'price histories'

    def __str__(self):
        return f'{self.product.name}: {self.old_price} -> {self.new_price}'
