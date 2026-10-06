from django.urls import path
from . import views

app_name = 'sales'

urlpatterns = [
    path('', views.SaleListView.as_view(), name='list'),
    path('add/', views.sale_create, name='add'),
    path('<int:pk>/receipt/', views.SaleDetailView.as_view(), name='receipt'),
    path('<int:pk>/delete/', views.sale_delete, name='delete'),
]
