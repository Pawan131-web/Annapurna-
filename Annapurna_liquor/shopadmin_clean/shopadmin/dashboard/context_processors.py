from django.conf import settings


def sidebar_alerts(request):
    """Adds common global context like frontend_url and low-stock count."""
    frontend_url = getattr(settings, 'FRONTEND_URL', 'http://127.0.0.1:8000').rstrip('/') + '/'
    ctx = {'frontend_url': frontend_url}
    if not request.user.is_authenticated:
        return ctx
    from django.db.models import F
    from products.models import Product
    low_stock_count = Product.objects.filter(
        is_deleted=False, quantity_in_stock__lte=F('low_stock_threshold')
    ).count()
    ctx['sidebar_low_stock_count'] = low_stock_count
    return ctx

