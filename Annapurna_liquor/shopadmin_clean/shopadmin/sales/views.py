import json
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import DetailView, ListView

from inventory.models import StockMovement
from products.models import Product
from .forms import SaleForm, SaleItemFormSet
from .models import Sale, SaleItem


class SaleListView(LoginRequiredMixin, ListView):
    model = Sale
    template_name = 'sales/sale_list.html'
    context_object_name = 'sales'
    paginate_by = 25

    def get_queryset(self):
        qs = Sale.objects.select_related('sold_by').prefetch_related('items__product')
        q = self.request.GET.get('q')
        date_from = self.request.GET.get('from')
        date_to = self.request.GET.get('to')
        if q:
            qs = qs.filter(invoice_number__icontains=q)
        if date_from:
            qs = qs.filter(sold_at__date__gte=date_from)
        if date_to:
            qs = qs.filter(sold_at__date__lte=date_to)
        return qs


class SaleDetailView(LoginRequiredMixin, DetailView):
    """Printable receipt / invoice view."""
    model = Sale
    template_name = 'sales/receipt.html'
    context_object_name = 'sale'


@transaction.atomic
def sale_create(request):
    active_products = Product.objects.filter(is_deleted=False, status='active', quantity_in_stock__gt=0).order_by('name')
    products_data = [
        {
            'id': p.pk,
            'name': p.name,
            'sku': p.sku,
            'price': float(p.selling_price),
            'stock': p.quantity_in_stock,
            'unit': p.get_unit_display()
        } for p in active_products
    ]

    if request.method == 'POST':
        sale_form = SaleForm(request.POST)
        formset = SaleItemFormSet(request.POST)
        if sale_form.is_valid() and formset.is_valid():
            lines = [f.cleaned_data for f in formset if f.cleaned_data and not f.cleaned_data.get('DELETE')]
            if not lines:
                messages.error(request, 'Add at least one product to the sale.')
            else:
                sale = sale_form.save(commit=False)
                sale.sold_by = request.user
                sale.save()
                for line in lines:
                    product = line['product']
                    quantity = line['quantity']
                    SaleItem.objects.create(
                        sale=sale, product=product, quantity=quantity,
                        unit_price=product.selling_price, unit_cost=product.cost_price,
                    )
                    before = product.quantity_in_stock
                    product.quantity_in_stock = before - quantity
                    product.save(update_fields=['quantity_in_stock'])
                    StockMovement.objects.create(
                        product=product, direction=StockMovement.Direction.OUT,
                        reason=StockMovement.Reason.SALE, quantity=quantity,
                        quantity_before=before, quantity_after=product.quantity_in_stock,
                        note=f'Sale {sale.invoice_number}', created_by=request.user,
                    )
                messages.success(request, f'Sale {sale.invoice_number} recorded.')
                return redirect('sales:receipt', pk=sale.pk)
    else:
        sale_form = SaleForm()
        formset = SaleItemFormSet()

    return render(request, 'sales/sale_form.html', {
        'sale_form': sale_form,
        'formset': formset,
        'products_data_json': json.dumps(products_data),
        'active_products': active_products,
    })


@transaction.atomic
def sale_delete(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    if request.method == 'POST':
        invoice_num = sale.invoice_number
        # Restore item stock quantities
        for item in sale.items.select_related('product'):
            product = item.product
            before = product.quantity_in_stock
            product.quantity_in_stock = before + item.quantity
            product.save(update_fields=['quantity_in_stock'])

            # Log stock movement return
            StockMovement.objects.create(
                product=product,
                direction=StockMovement.Direction.IN,
                reason=StockMovement.Reason.RETURN,
                quantity=item.quantity,
                quantity_before=before,
                quantity_after=product.quantity_in_stock,
                note=f'Cancelled sale {invoice_num}',
                created_by=request.user,
            )

        sale.delete()
        messages.success(request, f'Sale {invoice_num} deleted and item stock levels restored.')
        return redirect('sales:list')

    return render(request, 'sales/sale_confirm_delete.html', {'sale': sale})
