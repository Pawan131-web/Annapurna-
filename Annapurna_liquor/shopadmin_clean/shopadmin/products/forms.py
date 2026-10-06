from django import forms
from django.forms import inlineformset_factory

from categories.models import Category
from suppliers.models import Supplier
from .models import Product, ProductImage


class CategoryModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.display_name


class ProductForm(forms.ModelForm):
    category = CategoryModelChoiceField(
        queryset=Category.objects.select_related('parent').order_by('parent__name', 'name'),
        empty_label="Select Category"
    )
    supplier = forms.ModelChoiceField(
        queryset=Supplier.objects.all().order_by('name'),
        required=False,
        empty_label="Select Supplier",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Product
        fields = [
            'name', 'category', 'supplier', 'description',
            'cost_price', 'selling_price', 'quantity_in_stock', 'unit',
            'low_stock_threshold', 'status',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


ProductImageFormSet = inlineformset_factory(
    Product, ProductImage,
    fields=['image', 'is_primary'],
    extra=1,
    can_delete=True,
)


class QuickPriceForm(forms.Form):
    cost_price = forms.DecimalField(max_digits=12, decimal_places=2, required=False)
    selling_price = forms.DecimalField(max_digits=12, decimal_places=2, required=False)
