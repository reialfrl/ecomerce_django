from django.urls import path

from . import views

#Archivo presente en diversos modelos para registrar las urls de cada modulo.

app_name = 'carts'

urlpatterns = [
    path('', views.cart, name='cart'),
    path('add', views.add, name='add'),
    path('remove', views.remove, name='remove'),
]