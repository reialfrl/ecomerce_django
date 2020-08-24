from django.urls import path

from . import views

#Archivo presente en diversos modelos para registrar las urls de cada modulo.

app_name = 'products'

urlpatterns = [
    path('search', views.ProductSearchListView.as_view(), name='search'),
    path('<slug:slug>', views.ProductDetailView.as_view(), name='product'),
]