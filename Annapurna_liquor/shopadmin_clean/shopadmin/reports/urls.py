from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('sales/', views.sales_report, name='sales'),
    path('inventory/', views.inventory_report, name='inventory'),
    path('performance/', views.product_performance_report, name='performance'),
    path('profit/', views.profit_report, name='profit'),
]
