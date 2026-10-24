import json
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import DetailView, ListView

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse

from inventory.models import StockMovement
from products.models import Product
from .forms import SaleForm, SaleItemFormSet
from .models import Sale, SaleItem, OnlineOrder, OnlineOrderItem



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


# ==========================================
# ONLINE PURCHASE REQUESTS / ORDERS VIEWS
# ==========================================

class OrderListView(LoginRequiredMixin, ListView):
    model = OnlineOrder
    template_name = 'sales/order_list.html'
    context_object_name = 'orders'
    paginate_by = 25

    def get_queryset(self):
        qs = OnlineOrder.objects.prefetch_related('items__product').order_by('-created_at')
        q = self.request.GET.get('q', '').strip()
        status_val = self.request.GET.get('status', '').strip().lower()
        date_from = self.request.GET.get('from', '').strip()
        date_to = self.request.GET.get('to', '').strip()

        if q:
            qs = qs.filter(
                Q(order_number__icontains=q) |
                Q(customer_name__icontains=q) |
                Q(customer_phone__icontains=q) |
                Q(customer_email__icontains=q) |
                Q(delivery_address__icontains=q) |
                Q(items__product_name__icontains=q)
            ).distinct()

        if status_val and status_val != 'all':
            qs = qs.filter(status=status_val)

        if date_from:
            qs = qs.filter(created_at__date__gte=date_from)
        if date_to:
            qs = qs.filter(created_at__date__lte=date_to)

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        all_orders = OnlineOrder.objects.all()
        ctx['counts'] = {
            'all': all_orders.count(),
            'new': all_orders.filter(status=OnlineOrder.Status.NEW).count(),
            'contacted': all_orders.filter(status=OnlineOrder.Status.CONTACTED).count(),
            'completed': all_orders.filter(status=OnlineOrder.Status.COMPLETED).count(),
            'cancelled': all_orders.filter(status=OnlineOrder.Status.CANCELLED).count(),
        }
        ctx['status_choices'] = OnlineOrder.Status.choices
        ctx['current_status'] = self.request.GET.get('status', 'all')
        ctx['q'] = self.request.GET.get('q', '')
        ctx['date_from'] = self.request.GET.get('from', '')
        ctx['date_to'] = self.request.GET.get('to', '')
        return ctx


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = OnlineOrder
    template_name = 'sales/order_detail.html'
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['status_choices'] = OnlineOrder.Status.choices
        return ctx


@login_required
def order_update_status(request, pk):
    order = get_object_or_404(OnlineOrder, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        notes = request.POST.get('notes')

        valid_statuses = [c[0] for c in OnlineOrder.Status.choices]
        if new_status in valid_statuses:
            order.status = new_status
            if notes is not None:
                order.notes = notes.strip()
            order.save(update_fields=['status', 'notes', 'updated_at'])

            if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.GET.get('format') == 'json':
                return JsonResponse({
                    'status': 'success',
                    'new_status': order.status,
                    'status_display': order.get_status_display(),
                    'badge_class': order.get_status_badge_class(),
                })

            messages.success(request, f"Order {order.order_number} status updated to '{order.get_status_display()}'.")
        else:
            messages.error(request, f"Invalid status '{new_status}' provided.")

        next_url = request.POST.get('next') or request.GET.get('next')
        if next_url:
            return redirect(next_url)
        return redirect('sales:order_detail', pk=order.pk)

    return redirect('sales:order_detail', pk=order.pk)


@login_required
def order_delete(request, pk):
    order = get_object_or_404(OnlineOrder, pk=pk)
    if request.method == 'POST':
        order_num = order.order_number
        order.delete()
        messages.success(request, f"Order request {order_num} has been deleted.")
        return redirect('sales:order_list')
    return render(request, 'sales/order_confirm_delete.html', {'order': order})

