from django import forms
from products.models import Product
from suppliers.models import Supplier
from .models import StockMovement


class StockMovementForm(forms.Form):
    product = forms.ModelChoiceField(
        queryset=Product.objects.filter(is_deleted=False).order_by('name'),
        widget=forms.Select(attrs={'class': 'form-select'}),
        empty_label="Select Product"
    )
    direction = forms.ChoiceField(
        choices=StockMovement.Direction.choices,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    reason = forms.ChoiceField(
        choices=StockMovement.Reason.choices,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    quantity = forms.IntegerField(
        min_value=1,
        initial=1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '1'})
    )
    note = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Reference Note'})
    )

    def clean(self):
        cleaned = super().clean()
        product = cleaned.get('product')
        direction = cleaned.get('direction')
        quantity = cleaned.get('quantity')
        if product and direction == StockMovement.Direction.OUT and quantity and quantity > product.quantity_in_stock:
            raise forms.ValidationError(f'Only {product.quantity_in_stock} {product.get_unit_display()} available in stock.')
        return cleaned


class IncomingStockForm(forms.Form):
    product = forms.ModelChoiceField(
        queryset=Product.objects.filter(is_deleted=False).order_by('name'),
        widget=forms.Select(attrs={'class': 'form-select'}),
        empty_label="Select Product"
    )
    quantity = forms.IntegerField(
        min_value=1,
        initial=1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '1'})
    )
    supplier = forms.ModelChoiceField(
        queryset=Supplier.objects.all().order_by('name'),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        empty_label="Select Supplier"
    )
    cost_price = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Unit Cost Price'})
    )
    note = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Invoice PO Reference'})
    )
