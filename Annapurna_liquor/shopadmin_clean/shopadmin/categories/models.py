from django.db import models
from django.urls import reverse


class Category(models.Model):
    class Department(models.TextChoices):
        LIQUOR = 'liquor', 'Liquor'
        GROCERY = 'grocery', 'Grocery'
        BOTH = 'both', 'Both'

    name = models.CharField(max_length=120, unique=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subcategories')
    department = models.CharField(max_length=20, choices=Department.choices, default=Department.BOTH)
    description = models.TextField(blank=True)
    icon = models.ImageField(upload_to='categories/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['parent__name', 'name']
        verbose_name_plural = 'categories'

    def __str__(self):
        if self.parent:
            return f'{self.parent.name} › {self.name}'
        return self.name

    @property
    def display_name(self):
        if self.parent:
            return f'{self.parent.name} › {self.name}'
        return self.name

    def get_absolute_url(self):
        return reverse('categories:detail', args=[self.pk])

    @property
    def product_count(self):
        return self.products.filter(is_deleted=False).count()
