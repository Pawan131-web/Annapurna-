from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('', views.StockMovementListView.as_view(), name='list'),
    path('add/', views.StockMovementCreateView.as_view(), name='add'),
    path('receive/', views.receive_stock, name='receive'),
    path('<int:pk>/delete/', views.movement_delete, name='delete'),
]
