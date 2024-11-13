# homicidios/urls.py
from django.urls import path
from . import views

app_name = 'homicidios'  # Define el namespace

urlpatterns = [
    path('', views.dashboard, name='dashboard'),  # Ruta para el dashboard
    path('mostrar/', views.mostrar_homicidios, name='mostrar_homicidios'),
]
