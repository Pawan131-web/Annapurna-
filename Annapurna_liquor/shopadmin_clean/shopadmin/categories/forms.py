from django import forms
from .models import Category


class CategoryForm(forms.ModelForm):
    parent = forms.ModelChoiceField(
        queryset=Category.objects.filter(parent__isnull=True).order_by('name'),
        required=False,
        empty_label="Select Parent Category",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Category
        fields = ['name', 'parent', 'description', 'icon', 'is_active']
        labels = {
            'parent': 'Parent Category',
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Category Name', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Description', 'class': 'form-control'}),
        }
