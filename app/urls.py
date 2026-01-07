from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('login/', views.login_view, name='login'),
    path('registro/', views.registro, name='registro'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('solicitar/', views.solicitar_tramite, name='solicitar_tramite'),
    path('mis-solicitudes/', views.mis_solicitudes, name='mis_solicitudes'),
    path('logout/', views.logout_view, name='logout'),
]
