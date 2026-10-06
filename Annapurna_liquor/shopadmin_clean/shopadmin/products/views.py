from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import ProductForm, ProductImageFormSet
from .models import PriceHistory, Product


class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 20

    def get_queryset(self):
        qs = Product.objects.filter(is_deleted=False).select_related('category', 'supplier')
        q = self.request.GET.get('q')
        category = self.request.GET.get('category')
        supplier = self.request.GET.get('supplier')
        stock = self.request.GET.get('stock')
        sort = self.request.GET.get('sort', '-created_at')

        if q:
            qs = qs.filter(Q(name__icontains=q) | Q(sku__icontains=q))
        if category:
            qs = qs.filter(category_id=category)
        if supplier:
            qs = qs.filter(supplier_id=supplier)
        if stock == 'low':
            qs = qs.filter(quantity_in_stock__lte=F('low_stock_threshold'))
        if sort in ('name', '-name', 'selling_price', '-selling_price', 'quantity_in_stock', '-quantity_in_stock', 'created_at', '-created_at'):
            qs = qs.order_by(sort)
        return qs

    def get_context_data(self, **kwargs):
        from categories.models import Category
        from suppliers.models import Supplier
        ctx = super().get_context_data(**kwargs)
        ctx['categories'] = Category.objects.filter(is_active=True)
        ctx['suppliers'] = Supplier.objects.filter(is_active=True)
        ctx['current_sort'] = self.request.GET.get('sort', '-created_at')
        return ctx


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['price_history'] = self.object.price_history.all()[:10]
        ctx['stock_movements'] = self.object.stock_movements.all()[:10]
        return ctx


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.request.POST:
            ctx['image_formset'] = ProductImageFormSet(self.request.POST, self.request.FILES)
        else:
            ctx['image_formset'] = ProductImageFormSet()
        return ctx

    def form_valid(self, form):
        context = self.get_context_data()
        image_formset = context['image_formset']
        if image_formset.is_valid():
            self.object = form.save()
            image_formset.instance = self.object
            image_formset.save()
            messages.success(self.request, f'Product "{self.object.name}" created.')
            return redirect(self.object.get_absolute_url())
        return self.render_to_response(self.get_context_data(form=form))


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.request.POST:
            ctx['image_formset'] = ProductImageFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            ctx['image_formset'] = ProductImageFormSet(instance=self.object)
        return ctx

    def form_valid(self, form):
        old = Product.objects.get(pk=self.object.pk)
        context = self.get_context_data()
        image_formset = context['image_formset']
        if image_formset.is_valid():
            response = super().form_valid(form)
            image_formset.instance = self.object
            image_formset.save()
            self._log_price_changes(old, self.object)
            messages.success(self.request, f'Product "{self.object.name}" updated.')
            return response
        return self.render_to_response(self.get_context_data(form=form))

    def _log_price_changes(self, old, new):
        entries = []
        if old.cost_price != new.cost_price:
            entries.append(PriceHistory(product=new, price_type=PriceHistory.PriceType.COST,
                                         old_price=old.cost_price, new_price=new.cost_price,
                                         changed_by=self.request.user))
        if old.selling_price != new.selling_price:
            entries.append(PriceHistory(product=new, price_type=PriceHistory.PriceType.SELLING,
                                         old_price=old.selling_price, new_price=new.selling_price,
                                         changed_by=self.request.user))
        if entries:
            PriceHistory.objects.bulk_create(entries)


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    """Soft delete: flips is_deleted instead of removing the row."""
    model = Product
    template_name = 'products/product_confirm_delete.html'
    success_url = reverse_lazy('products:list')

    def form_valid(self, form):
        self.object = self.get_object()
        self.object.is_deleted = True
        self.object.save(update_fields=['is_deleted'])
        messages.success(self.request, f'Product "{self.object.name}" deleted.')
        return redirect(self.success_url)


class QuickPriceUpdateView(LoginRequiredMixin, View):
    """AJAX endpoint used by the inline quick-edit modal on the product list."""

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        cost_price = request.POST.get('cost_price')
        selling_price = request.POST.get('selling_price')
        entries = []
        if cost_price and float(cost_price) != float(product.cost_price):
            entries.append(PriceHistory(product=product, price_type=PriceHistory.PriceType.COST,
                                         old_price=product.cost_price, new_price=cost_price,
                                         changed_by=request.user))
            product.cost_price = cost_price
        if selling_price and float(selling_price) != float(product.selling_price):
            entries.append(PriceHistory(product=product, price_type=PriceHistory.PriceType.SELLING,
                                         old_price=product.selling_price, new_price=selling_price,
                                         changed_by=request.user))
            product.selling_price = selling_price
        product.save()
        PriceHistory.objects.bulk_create(entries)
        return JsonResponse({
            'ok': True,
            'cost_price': str(product.cost_price),
            'selling_price': str(product.selling_price),
        })
