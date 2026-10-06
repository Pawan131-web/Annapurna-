from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('categories', views.CategoryViewSet, basename='api-categories')
router.register('suppliers', views.SupplierViewSet, basename='api-suppliers')
router.register('products', views.ProductViewSet, basename='api-products')
router.register('sales', views.SaleViewSet, basename='api-sales')
router.register('orders', views.OnlineOrderViewSet, basename='api-orders')

app_name = 'api'

urlpatterns = [
    path('', include(router.urls)),
]
