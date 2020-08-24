from django.urls import path

from . import views

#Archivo presente en diversos modelos para registrar las urls de cada modulo.

app_name = 'promo_codes'

urlpatterns = [
    path('validate', views.validate, name='validate')
]