from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.db.models import F, Sum
from django.shortcuts import render
from django.utils import timezone

from products.models import Product
from sales.models import Sale, SaleItem

from .utils import export_csv, export_xlsx


def _date_range(request):
    today = timezone.localdate()
    date_from = request.GET.get('from') or (today - timedelta(days=29)).isoformat()
    date_to = request.GET.get('to') or today.isoformat()
    return date_from, date_to


@login_required
def sales_report(request):
    date_from, date_to = _date_range(request)
    sales = (
        Sale.objects.filter(sold_at__date__gte=date_from, sold_at__date__lte=date_to)
        .prefetch_related('items')
        .order_by('-sold_at')
    )
    rows = [(s.invoice_number, s.customer_name, s.get_payment_method_display(),
             s.sold_at.strftime('%Y-%m-%d %H:%M'), str(s.total_amount)) for s in sales]

    fmt = request.GET.get('export')
    header = ['Invoice', 'Customer', 'Payment Method', 'Date', 'Total']
    if fmt == 'csv':
        return export_csv('sales_report', header, rows)
    if fmt == 'xlsx':
        return export_xlsx('sales_report', header, rows, 'Sales')

    total_revenue = sum((s.total_amount for s in sales), 0)
    return render(request, 'reports/sales_report.html', {
        'sales': sales, 'date_from': date_from, 'date_to': date_to, 'total_revenue': total_revenue,
    })


@login_required
def inventory_report(request):
    products = Product.objects.filter(is_deleted=False).select_related('category', 'supplier').prefetch_related('images')
    only_low = request.GET.get('low') == '1'
    if only_low:
        products = products.filter(quantity_in_stock__lte=F('low_stock_threshold'))

    rows = [(p.name, p.category.name, p.quantity_in_stock, p.low_stock_threshold,
             str(p.cost_price), str(p.selling_price)) for p in products]
    header = ['Name', 'Category', 'Qty in Stock', 'Low Stock Threshold', 'Cost Price', 'Selling Price']

    fmt = request.GET.get('export')
    if fmt == 'csv':
        return export_csv('inventory_report', header, rows)
    if fmt == 'xlsx':
        return export_xlsx('inventory_report', header, rows, 'Inventory')

    return render(request, 'reports/inventory_report.html', {'products': products, 'only_low': only_low})


@login_required
def product_performance_report(request):
    date_from, date_to = _date_range(request)
    items = SaleItem.objects.filter(sale__sold_at__date__gte=date_from, sale__sold_at__date__lte=date_to)

    best_qs = (items.values('product_id')
               .annotate(qty=Sum('quantity'), revenue=Sum(F('unit_price') * F('quantity')))
               .order_by('-qty')[:15])

    worst_qs = (items.values('product_id')
                .annotate(qty=Sum('quantity'), revenue=Sum(F('unit_price') * F('quantity')))
                .order_by('qty')[:15])

    product_ids = {r['product_id'] for r in best_qs} | {r['product_id'] for r in worst_qs}
    products_map = Product.objects.filter(id__in=product_ids).prefetch_related('images').in_bulk()

    best = []
    for r in best_qs:
        p = products_map.get(r['product_id'])
        best.append({
            'product': p,
            'name': p.name if p else 'Unknown Product',
            'qty': r['qty'],
            'revenue': r['revenue'],
        })

    worst = []
    for r in worst_qs:
        p = products_map.get(r['product_id'])
        worst.append({
            'product': p,
            'name': p.name if p else 'Unknown Product',
            'qty': r['qty'],
            'revenue': r['revenue'],
        })

    return render(request, 'reports/product_performance_report.html', {
        'best': best, 'worst': worst, 'date_from': date_from, 'date_to': date_to,
    })


@login_required
def profit_report(request):
    date_from, date_to = _date_range(request)
    items = SaleItem.objects.filter(sale__sold_at__date__gte=date_from, sale__sold_at__date__lte=date_to)

    rows_qs = (items.values('product_id')
               .annotate(qty=Sum('quantity'),
                         revenue=Sum(F('unit_price') * F('quantity')),
                         cost=Sum(F('unit_cost') * F('quantity')))
               .order_by('-revenue'))

    product_ids = {r['product_id'] for r in rows_qs}
    products_map = Product.objects.filter(id__in=product_ids).prefetch_related('images').in_bulk()

    rows = []
    total_revenue = total_cost = 0
    for r in rows_qs:
        p = products_map.get(r['product_id'])
        profit = (r['revenue'] or 0) - (r['cost'] or 0)
        total_revenue += r['revenue'] or 0
        total_cost += r['cost'] or 0
        rows.append({
            'product': p,
            'name': p.name if p else 'Unknown Product',
            'qty': r['qty'],
            'revenue': r['revenue'],
            'cost': r['cost'],
            'profit': profit,
        })

    fmt = request.GET.get('export')
    if fmt in ('csv', 'xlsx'):
        header = ['Product', 'Qty Sold', 'Revenue', 'Cost', 'Profit']
        export_rows = [(r['name'], r['qty'], str(r['revenue']), str(r['cost']), str(r['profit'])) for r in rows]
        if fmt == 'csv':
            return export_csv('profit_report', header, export_rows)
        return export_xlsx('profit_report', header, export_rows, 'Profit')

    return render(request, 'reports/profit_report.html', {
        'rows': rows, 'date_from': date_from, 'date_to': date_to,
        'total_revenue': total_revenue, 'total_cost': total_cost, 'total_profit': total_revenue - total_cost,
    })
