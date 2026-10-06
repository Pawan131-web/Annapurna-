from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.DashboardHomeView.as_view(), name='home'),
    path('settings/', views.SettingsView.as_view(), name='settings'),
    path('settings/password/', views.AdminPasswordChangeView.as_view(), name='change_password'),
    path('settings/profile/', views.ProfileUpdateView.as_view(), name='profile_update'),
]
