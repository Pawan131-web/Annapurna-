from django.urls import path
from . import views

app_name = 'sales'

urlpatterns = [
    path('', views.SaleListView.as_view(), name='list'),
    path('add/', views.sale_create, name='add'),
    path('<int:pk>/receipt/', views.SaleDetailView.as_view(), name='receipt'),
    path('<int:pk>/delete/', views.sale_delete, name='delete'),
    # Purchase Requests / Orders
    path('orders/', views.OrderListView.as_view(), name='order_list'),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('orders/<int:pk>/status/', views.order_update_status, name='order_update_status'),
    path('orders/<int:pk>/delete/', views.order_delete, name='order_delete'),
]
