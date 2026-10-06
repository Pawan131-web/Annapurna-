from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import RedirectView
from .storefront import serve_storefront

urlpatterns = [
    path('django-admin/login/', RedirectView.as_view(pattern_name='accounts:login', permanent=False, query_string=True)),
    path('django-admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('categories/', include('categories.urls')),
    path('suppliers/', include('suppliers.urls')),
    path('products/', include('products.urls')),
    path('inventory/', include('inventory.urls')),
    path('sales/', include('sales.urls')),
    path('reports/', include('reports.urls')),
    path('api/', include('api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Unified Single-Port Storefront Routes (Liquor & Grocery store frontend)
urlpatterns += [
    path('', serve_storefront, {'path': ''}, name='storefront-root'),
    re_path(r'^(?P<path>.+)$', serve_storefront, name='storefront-files'),
]
