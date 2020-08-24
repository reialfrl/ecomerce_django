from .models import Order

from django.urls import reverse

def get_or_create_order(cart, request):
    #Función para obtener o crear una orden.
    order = cart.order

    if order is None and request.user.is_authenticated:
        order = Order.objects.create(cart=cart, user=request.user)

    if order:
        request.session['order_id'] = order.order_id

    return order

def breadcrumb(products=True, address=False, payment=False, confirmation=False):
    return [
        {'title': 'Products', 'active': products, 'url': reverse('orders:order')},
        {'title': 'Address', 'active': address, 'url': reverse('orders:address')},
        {'title': 'Payment', 'active': payment, 'url': reverse('orders:payment')},
        {'title': 'Confirmation', 'active': confirmation, 'url': reverse('orders:confirm')},
    ]

def destroy_order(request):
    request.session['order_id'] = None