from django.contrib import admin
from .models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'product_count', 'is_active', 'created_at')
    search_fields = ('name',)
    list_filter = ('department', 'is_active')

