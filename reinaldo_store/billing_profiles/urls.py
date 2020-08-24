from django.urls import path

from . import views

#Archivo presente en diversos modelos para registrar las urls de cada modulo.

app_name = 'billing_profiles'

urlpatterns = [
    path('', views.BillingProfileListView.as_view(), name='billing_profiles'),
    path('new', views.create, name='create'),
]