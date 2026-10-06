from django.db import models
from django.urls import reverse


class Supplier(models.Model):
    name = models.CharField(max_length=150, unique=True)
    contact_person = models.CharField(max_length=150, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('suppliers:detail', args=[self.pk])

    @property
    def product_count(self):
        return self.products.filter(is_deleted=False).count()
