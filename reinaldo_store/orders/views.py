import threading

from django.contrib import messages

from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404

from django.db import transaction

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.db.models.query import EmptyQuerySet
from django.views.generic.list import ListView

from shipping_addresses.models import ShippingAddress

from .decorators import validate_cart_and_order

from .mails import Mail

from charges.models import Charge
from .models import Order

from .utils import breadcrumb
from .utils import destroy_order
from .utils import get_or_create_order

from carts.utils import destroy_cart
from carts.utils import get_or_create_cart


class OrderListView(LoginRequiredMixin, ListView):
    #Clase para obtener la lista de las ordenes.
    login_url = 'login'
    template_name = 'orders/orders.html'

    def get_queryset(self):
        return self.request.user.orders_completed()

@login_required(login_url='login')
@validate_cart_and_order
def order(request, cart, order):
    #Función si la orden no tiene un producto redirecciona al carrito.

    if not cart.has_products():
        return redirect('carts:cart')

    return render(request, 'orders/order.html', {
        'cart': cart,
        'order': order,        
        'breadcrumb': breadcrumb(),
    }) 

@login_required(login_url='login')
@validate_cart_and_order
def address(request, cart, order):
    #Función para obtener una dirección y asociara a una orden.

    if not cart.has_products():
        return redirect('carts:cart')

    shipping_address = order.get_or_set_shipping_address()
    can_choose_address = request.user.has_shipping_addresses()

    return render(request, 'orders/address.html', {
        'cart': cart,
        'order': order,
        'can_choose_address': can_choose_address,
        'shipping_address': shipping_address,
        'breadcrumb': breadcrumb(address=True),
    })

@login_required(login_url='login')
def select_address(request):
    #Función para poder seleccionar una dirección.
    shipping_addresses = request.user.addresses

    return render(request, 'orders/select_address.html', {
        'breadcrumb': breadcrumb(address=True),
        'shipping_addresses': shipping_addresses
    })
@login_required(login_url='login')
@validate_cart_and_order
def check_address(request, cart, order, pk):
    #Función para poder escoger una dirección.
    shipping_address = get_object_or_404(ShippingAddress, pk=pk)

    if request.user.id != shipping_address.user_id:
        return redirect('carts:cart')

    order.update_shipping_address(shipping_address)

    return redirect('orders:address')

@login_required(login_url='login')
@validate_cart_and_order
def payment(request, cart, order):
    #Función para poder escoger un metodo de pago en la orden.

    if not cart.has_products() or order.shipping_address is None:
        return redirect('carts:cart')

    billing_profile = order.get_or_set_billing_profile()

    return render(request, 'orders/payment.html', {
        'cart': cart,
        'order': order,
        'billing_profile': billing_profile,
        'breadcrumb': breadcrumb(address=True, payment=True),
    })
@login_required(login_url='login')
@validate_cart_and_order
def confirm(request, cart, order):
    #Función para poder confirmar una orden.

    if not cart.has_products() or order.shipping_address is None or order.billing_profile is None:
        return redirect('carts:cart')
    
    shipping_address = order.shipping_address

    if shipping_address is None:
        return redirect('carts:cart')

    return render(request, 'orders/confirm.html', {
        'cart': cart,
        'order': order,
        'shipping_address': shipping_address,
        'breadcrumb': breadcrumb(address=True, payment=True, confirmation=True),

    })

@login_required(login_url='login')
@validate_cart_and_order
def cancel(request, cart, order):
    #Función para poder cancelar una orden.

    if request.user.id != order.user_id:
        return redirect('carts:cart')

    order.cancel()

    destroy_cart(request)
    destroy_order(request)

    messages.error(request, 'Order canceled')
    return redirect('index')

@login_required(login_url='login')
@validate_cart_and_order
def complete(request, cart, order):
    #Función para poder completar una orden.
    if request.user.id != order.user_id:
        return redirect('carts:cart')    

    charge = Charge.objects.create_charge(order)
    if charge:
        with transaction.atomic():
            order.complete()

            thread = threading.Thread(target=Mail.send_complete_order, args=(
                order, request.user
            ))
            thread.start()

            destroy_cart(request)
            destroy_order(request)

            messages.success(request, 'Order completed successfully')
    return redirect('index')
