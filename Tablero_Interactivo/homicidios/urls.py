# homicidios/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('homicidios/', views.mostrar_homicidios, name='mostrar_homicidios'),
]
