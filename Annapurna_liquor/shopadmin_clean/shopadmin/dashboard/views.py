import json
from datetime import timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F, Sum, Count
from django.db.models.functions import TruncDate
from django.shortcuts import redirect
from django.utils import timezone
from django.views.generic import TemplateView, View

from categories.models import Category
from inventory.models import StockMovement
from products.models import Product
from sales.models import Sale, SaleItem
from suppliers.models import Supplier


class DashboardHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/home.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        today = timezone.localdate()

        products_count = Product.objects.filter(is_deleted=False).count()
        categories_count = Category.objects.filter(is_active=True).count()
        suppliers_count = Supplier.objects.filter(is_active=True).count()

        low_stock_qs = Product.objects.filter(is_deleted=False, quantity_in_stock__lte=F('low_stock_threshold'))
        low_stock_count = low_stock_qs.count()

        total_sales_qs = Sale.objects.all()
        total_sales_sum = sum((s.total_amount for s in total_sales_qs), 0)

        display_sales_amount = f"{float(total_sales_sum):,.0f}" if total_sales_sum > 0 else "0"

        ctx.update({
            'total_products': products_count,
            'total_sales_display': display_sales_amount,
            'low_stock_count': low_stock_count,
            'total_suppliers': suppliers_count,
            'sidebar_low_stock_count': low_stock_count,

            # Trends
            'products_trend': f'{products_count} active',
            'sales_trend': f'{total_sales_qs.count()} orders',
            'low_stock_trend': f'{low_stock_count} items',
            'suppliers_trend': f'{suppliers_count} active',

            'date_range_label': f"{today - timedelta(days=6):%b %d} - {today:%b %d, %Y}",
            'sales_overview_json': json.dumps(self._sales_overview_trend()),
            'category_sales_json': json.dumps(self._category_sales_data()),
            'best_sellers_list': self._get_best_sellers(),
            'low_stock_list': self._get_low_stock_items(),
            'recent_sales_list': self._get_recent_sales(),
        })
        return ctx

    def _sales_overview_trend(self):
        """Returns trend data for 7d, 30d, 3m, 1y for Revenue & Orders from database."""
        today = timezone.localdate()

        def get_daily_data(days):
            start = today - timedelta(days=days - 1)
            labels = [(start + timedelta(days=i)).strftime('%b %d') for i in range(days)]
            sales = (
                SaleItem.objects.filter(sale__sold_at__date__gte=start)
                .annotate(day=TruncDate('sale__sold_at'))
                .values('day')
                .annotate(revenue=Sum(F('unit_price') * F('quantity')), orders=Count('sale', distinct=True))
                .order_by('day')
            )
            db_by_day = {r['day']: (float(r['revenue'] or 0), int(r['orders'] or 0)) for r in sales}
            revenue_data, orders_data = [], []
            for i in range(days):
                d = start + timedelta(days=i)
                rev, ords = db_by_day.get(d, (0, 0))
                revenue_data.append(rev)
                orders_data.append(ords)
            return {'labels': labels, 'revenue': revenue_data, 'orders': orders_data}

        def get_3m_data():
            weeks = 12
            start = today - timedelta(weeks=weeks - 1)
            sales = (
                SaleItem.objects.filter(sale__sold_at__date__gte=start)
                .annotate(day=TruncDate('sale__sold_at'))
                .values('day')
                .annotate(revenue=Sum(F('unit_price') * F('quantity')), orders=Count('sale', distinct=True))
                .order_by('day')
            )
            db_by_day = {r['day']: (float(r['revenue'] or 0), int(r['orders'] or 0)) for r in sales}
            labels, revenue_data, orders_data = [], [], []
            for w in range(weeks):
                w_start = start + timedelta(weeks=w)
                labels.append(w_start.strftime('%b %d'))
                w_rev, w_ords = 0.0, 0
                for i in range(7):
                    d = w_start + timedelta(days=i)
                    if d <= today:
                        rev, ords = db_by_day.get(d, (0, 0))
                        w_rev += rev
                        w_ords += ords
                revenue_data.append(w_rev)
                orders_data.append(w_ords)
            return {'labels': labels, 'revenue': revenue_data, 'orders': orders_data}

        def get_1y_data():
            one_year_ago = today - timedelta(days=365)
            sales = (
                SaleItem.objects.filter(sale__sold_at__date__gte=one_year_ago)
                .annotate(day=TruncDate('sale__sold_at'))
                .values('day')
                .annotate(revenue=Sum(F('unit_price') * F('quantity')), orders=Count('sale', distinct=True))
                .order_by('day')
            )
            db_by_day = {r['day']: (float(r['revenue'] or 0), int(r['orders'] or 0)) for r in sales}
            labels, revenue_data, orders_data = [], [], []
            for m in range(11, -1, -1):
                y = today.year
                mon = today.month - m
                while mon <= 0:
                    mon += 12
                    y -= 1
                m_label = timezone.datetime(y, mon, 1).strftime('%b %Y') if (m == 11 or mon == 1) else timezone.datetime(y, mon, 1).strftime('%b')
                labels.append(m_label)
                m_rev, m_ords = 0.0, 0
                for d, (rev, ords) in db_by_day.items():
                    if d.year == y and d.month == mon:
                        m_rev += rev
                        m_ords += ords
                revenue_data.append(m_rev)
                orders_data.append(m_ords)
            return {'labels': labels, 'revenue': revenue_data, 'orders': orders_data}

        return {
            '7d': get_daily_data(7),
            '30d': get_daily_data(30),
            '3m': get_3m_data(),
            '1y': get_1y_data(),
        }

    def _category_sales_data(self):
        """Returns category distribution for donut chart strictly from real sales."""
        rows = (
            SaleItem.objects.values('product__category__name')
            .annotate(total=Sum(F('unit_price') * F('quantity')))
            .order_by('-total')
        )
        
        labels, values = [], []
        for r in rows:
            if r['product__category__name']:
                labels.append(r['product__category__name'])
                values.append(float(r['total'] or 0))

        total_sum = sum(values)
        if total_sum > 0:
            percentages = [round((v / total_sum) * 100) for v in values]
            total_display = f"Rs. {total_sum:,.0f}"
        else:
            labels = [c.name for c in Category.objects.filter(is_active=True)]
            values = [0] * len(labels)
            percentages = [0] * len(labels)
            total_display = "Rs. 0"

        colors = ['#D4A359', '#52C478', '#E5C158', '#C59347', '#E07A5F', '#8C7F6A']

        categories_list = []
        for i, label in enumerate(labels):
            categories_list.append({
                'name': label,
                'percentage': percentages[i] if i < len(percentages) else 0,
                'color': colors[i % len(colors)],
            })

        return {
            'labels': labels,
            'data': values,
            'colors': colors[:len(labels)],
            'total_display': total_display,
            'categories_list': categories_list,
        }

    def _get_best_sellers(self):
        db_items = (
            SaleItem.objects.values('product__pk', 'product__name', 'product__category__name')
            .annotate(sold=Sum('quantity'), revenue=Sum(F('unit_price') * F('quantity')))
            .order_by('-sold')[:5]
        )
        
        result = []
        for idx, item in enumerate(db_items, 1):
            prod = Product.objects.filter(pk=item['product__pk']).first()
            img_url = prod.primary_image.image.url if (prod and prod.primary_image) else None
            cat_name = item['product__category__name'] or 'General'
            cat_code = cat_name.lower()
            result.append({
                'index': idx,
                'name': item['product__name'],
                'category': cat_name,
                'category_code': cat_code,
                'sold': item['sold'],
                'revenue': f"{float(item['revenue'] or 0):,.0f}",
                'image_url': img_url,
            })

        return result

    def _get_low_stock_items(self):
        db_items = Product.objects.filter(is_deleted=False, quantity_in_stock__lte=F('low_stock_threshold')).select_related('category').prefetch_related('images')[:5]
        
        result = []
        for item in db_items:
            cat_name = item.category.name if item.category else 'General'
            is_critical = item.quantity_in_stock <= 3
            img_url = item.primary_image.image.url if item.primary_image else None
            result.append({
                'name': item.name,
                'category': cat_name,
                'category_code': cat_name.lower(),
                'stock': item.quantity_in_stock,
                'status': 'Critical' if is_critical else 'Low',
                'is_critical': is_critical,
                'image_url': img_url,
            })

        return result

    def _get_recent_sales(self):
        db_sales = Sale.objects.prefetch_related('items__product').order_by('-sold_at')[:5]
        
        result = []
        for sale in db_sales:
            first_item = sale.items.first()
            p_name = first_item.product.name if first_item else 'General Items'
            qty = first_item.quantity if first_item else 1
            result.append({
                'order_id': f"#{sale.invoice_number.replace('INV-', 'ORD-')}",
                'product': p_name,
                'qty': qty,
                'amount': f"{float(sale.total_amount):,.0f}",
                'status': 'Completed',
                'pk': sale.pk,
            })

        return result


class SettingsView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/settings.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        import sys, platform, django
        from django.conf import settings as django_settings

        ctx['store_name'] = 'Annapurna Groceries & Liquor'
        ctx['store_email'] = 'contact@annapurnastore.com'
        ctx['store_phone'] = '+977 9801032139'
        ctx['store_address'] = 'Kathmandu, Nepal'
        ctx['currency'] = 'NPR (Rs.)'
        ctx['timezone'] = getattr(django_settings, 'TIME_ZONE', 'Asia/Kathmandu')
        ctx['frontend_url'] = getattr(django_settings, 'FRONTEND_URL', 'http://127.0.0.1:8000')

        # System environment information
        ctx['python_version'] = platform.python_version()
        ctx['django_version'] = django.get_version()
        ctx['debug_mode'] = getattr(django_settings, 'DEBUG', True)
        ctx['db_engine'] = django_settings.DATABASES['default']['ENGINE'].split('.')[-1]

        # Statistics summary
        ctx['total_products'] = Product.objects.filter(is_deleted=False).count()
        ctx['total_sales'] = Sale.objects.count()
        ctx['total_suppliers'] = Supplier.objects.count()
        return ctx


class AdminPasswordChangeView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        from django.contrib import messages
        from django.contrib.auth import update_session_auth_hash

        old_password = request.POST.get('old_password', '')
        new_password = request.POST.get('new_password', '')
        confirm_password = request.POST.get('confirm_password', '')

        if not request.user.check_password(old_password):
            messages.error(request, 'Current password entered is incorrect.')
            return redirect('dashboard:settings')

        if len(new_password) < 6:
            messages.error(request, 'New password must be at least 6 characters long.')
            return redirect('dashboard:settings')

        if new_password != confirm_password:
            messages.error(request, 'New password and confirmation password do not match.')
            return redirect('dashboard:settings')

        request.user.set_password(new_password)
        request.user.save()
        update_session_auth_hash(request, request.user)

        messages.success(request, 'Password updated successfully! Your active session is preserved.')
        return redirect('dashboard:settings')


class ProfileUpdateView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        from django.contrib import messages
        from accounts.models import Profile

        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()

        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        if email:
            user.email = email
        user.save()

        profile, _ = Profile.objects.get_or_create(user=user)
        if phone:
            profile.phone = phone
            profile.save()

        messages.success(request, 'Account profile information updated successfully.')
        return redirect('dashboard:settings')

