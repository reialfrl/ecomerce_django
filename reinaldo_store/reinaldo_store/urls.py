from django.contrib import admin

from django.urls import path
from django.urls import include

from django.conf.urls.static import static
from django.conf import settings

from . import views

from products .views import ProductListView

#Archivo presente en diversos modelos para registrar las urls de cada modulo.

urlpatterns = [
    path('', ProductListView.as_view(), name='index'),
    path('users/login', views.login_view, name='login'),
    path('users/logout', views.logout_view, name='logout'),
    path('users/register', views.register, name='register'),
    path('admin/', admin.site.urls),
    path('products/', include('products.urls')),
    path('carts/', include('carts.urls')),
    path('orders/', include('orders.urls')),
    path('addresses/', include('shipping_addresses.urls')),
    path('codes/', include('promo_codes.urls')),
    path('payments/', include('billing_profiles.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)