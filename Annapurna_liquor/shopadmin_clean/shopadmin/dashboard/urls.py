from django.urls import path
from . import views

app_name = 'dashboard'

from django.views.generic import RedirectView

urlpatterns = [
    path('', views.DashboardHomeView.as_view(), name='home'),
    path('orders/', RedirectView.as_view(pattern_name='sales:order_list', permanent=False), name='orders_redirect'),
    path('settings/', views.SettingsView.as_view(), name='settings'),
    path('settings/password/', views.AdminPasswordChangeView.as_view(), name='change_password'),
    path('settings/profile/', views.ProfileUpdateView.as_view(), name='profile_update'),
]
