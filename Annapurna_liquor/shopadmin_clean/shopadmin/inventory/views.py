from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView

from products.models import Product
from .forms import IncomingStockForm, StockMovementForm
from .models import StockMovement


class StockMovementListView(LoginRequiredMixin, ListView):
    model = StockMovement
    template_name = 'inventory/movement_list.html'
    context_object_name = 'movements'
    paginate_by = 25

    def get_queryset(self):
        qs = StockMovement.objects.select_related('product', 'created_by').prefetch_related('product__images')
        product = self.request.GET.get('product')
        reason = self.request.GET.get('reason')
        direction = self.request.GET.get('direction')
        if product:
            qs = qs.filter(product_id=product)
        if reason:
            qs = qs.filter(reason=reason)
        if direction:
            qs = qs.filter(direction=direction)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        base_qs = StockMovement.objects.all()
        
        context['total_incoming_qty'] = base_qs.filter(direction=StockMovement.Direction.IN).aggregate(s=Sum('quantity'))['s'] or 0
        context['total_outgoing_qty'] = base_qs.filter(direction=StockMovement.Direction.OUT).aggregate(s=Sum('quantity'))['s'] or 0
        context['total_inventory_units'] = Product.objects.filter(is_deleted=False).aggregate(s=Sum('quantity_in_stock'))['s'] or 0
        
        # Slices for tabs
        context['incoming_movements'] = base_qs.filter(direction=StockMovement.Direction.IN).select_related('product', 'created_by').prefetch_related('product__images')[:25]
        context['outgoing_movements'] = base_qs.filter(direction=StockMovement.Direction.OUT).select_related('product', 'created_by').prefetch_related('product__images')[:25]
        
        return context


class StockMovementCreateView(LoginRequiredMixin, FormView):
    form_class = StockMovementForm
    template_name = 'inventory/movement_form.html'
    success_url = reverse_lazy('inventory:list')

    @transaction.atomic
    def form_valid(self, form):
        product = form.cleaned_data['product']
        direction = form.cleaned_data['direction']
        quantity = form.cleaned_data['quantity']
        reason = form.cleaned_data['reason']
        note = form.cleaned_data['note']

        before = product.quantity_in_stock
        after = before + quantity if direction == StockMovement.Direction.IN else before - quantity
        product.quantity_in_stock = after
        product.save(update_fields=['quantity_in_stock'])

        StockMovement.objects.create(
            product=product, direction=direction, reason=reason, quantity=quantity,
            quantity_before=before, quantity_after=after, note=note, created_by=self.request.user,
        )
        messages.success(self.request, f'Stock {direction} recorded for "{product.name}".')
        return redirect(self.success_url)


@transaction.atomic
def receive_stock(request):
    if request.method == 'POST':
        form = IncomingStockForm(request.POST)
        if form.is_valid():
            product = form.cleaned_data['product']
            quantity = form.cleaned_data['quantity']
            supplier = form.cleaned_data.get('supplier')
            cost_price = form.cleaned_data.get('cost_price')
            note = form.cleaned_data.get('note', '')

            before = product.quantity_in_stock
            after = before + quantity
            product.quantity_in_stock = after

            update_fields = ['quantity_in_stock']
            if cost_price and cost_price > 0:
                product.cost_price = cost_price
                update_fields.append('cost_price')

            product.save(update_fields=update_fields)

            full_note = f'Supplier: {supplier.name}' if supplier else ''
            if note:
                full_note = f'{full_note} | {note}' if full_note else note

            StockMovement.objects.create(
                product=product,
                direction=StockMovement.Direction.IN,
                reason=StockMovement.Reason.PURCHASE,
                quantity=quantity,
                quantity_before=before,
                quantity_after=after,
                note=full_note,
                created_by=request.user,
            )

            messages.success(request, f'Successfully received {quantity} units of "{product.name}". Stock updated to {after}.')
            return redirect('inventory:list')
    else:
        form = IncomingStockForm()

    return render(request, 'inventory/incoming_form.html', {'form': form})


@transaction.atomic
def movement_delete(request, pk):
    movement = get_object_or_404(StockMovement.objects.select_related('product'), pk=pk)
    if request.method == 'POST':
        product = movement.product
        qty = movement.quantity
        p_name = product.name
        
        # Revert product stock level
        if movement.direction == StockMovement.Direction.IN:
            product.quantity_in_stock = max(0, product.quantity_in_stock - qty)
        else:
            product.quantity_in_stock += qty
        product.save(update_fields=['quantity_in_stock'])

        movement.delete()
        messages.success(request, f'Stock movement entry for "{p_name}" deleted and stock level adjusted.')
        return redirect('inventory:list')

    return render(request, 'inventory/movement_confirm_delete.html', {'movement': movement})
