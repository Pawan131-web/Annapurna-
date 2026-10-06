from django import forms
from django.forms import formset_factory
from products.models import Product
from .models import Sale


class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['customer_name', 'customer_phone', 'payment_method', 'note']
        widgets = {
            'customer_name': forms.TextInput(attrs={'placeholder': 'Customer Name', 'class': 'form-control'}),
            'customer_phone': forms.TextInput(attrs={'placeholder': 'Phone Number', 'class': 'form-control'}),
            'payment_method': forms.Select(attrs={'class': 'form-select'}),
            'note': forms.TextInput(attrs={'placeholder': 'Note or Remarks', 'class': 'form-control'}),
        }


class SaleItemLineForm(forms.Form):
    product = forms.ModelChoiceField(
        queryset=Product.objects.filter(is_deleted=False, status='active', quantity_in_stock__gt=0).order_by('name'),
        widget=forms.Select(attrs={'class': 'form-select product-select'}),
        empty_label="Select Product"
    )
    quantity = forms.IntegerField(
        min_value=1,
        initial=1,
        widget=forms.NumberInput(attrs={'class': 'form-control qty-input', 'min': '1', 'value': '1'})
    )

    def clean(self):
        cleaned = super().clean()
        product = cleaned.get('product')
        quantity = cleaned.get('quantity')
        if product and quantity and quantity > product.quantity_in_stock:
            raise forms.ValidationError(
                f'Only {product.quantity_in_stock} {product.get_unit_display()} of "{product.name}" left in stock.'
            )
        return cleaned


SaleItemFormSet = formset_factory(SaleItemLineForm, extra=1, can_delete=True)
