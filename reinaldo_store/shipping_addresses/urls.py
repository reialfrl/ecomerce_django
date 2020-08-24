from django.urls import path 

from . import views

#Archivo presente en diversos modelos para registrar las urls de cada modulo.

app_name = 'shipping_addresses'

urlpatterns = [
    path('', views.ShippingAddressListView.as_view(), name='shipping_addresses'),
    path('new', views.create, name='create'),
    path('edit/<int:pk>', views.ShippingAdressUpdateView.as_view(), name='update'),
    path('delete/<int:pk>', views.ShippingAdressDeleteView.as_view(), name='delete'),
    path('default/<int:pk>', views.default, name='default'),
]
