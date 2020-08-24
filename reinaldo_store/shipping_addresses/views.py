from django.contrib import messages

from django.http import HttpResponseRedirect

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

from django.shortcuts import render
from django.shortcuts import reverse
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404

from django.views.generic import ListView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView

from django.urls import reverse_lazy

from .models import ShippingAddress

from .forms import ShippingAddressForm

from carts.utils import get_or_create_cart
from orders.utils import get_or_create_order

class ShippingAddressListView(LoginRequiredMixin, ListView):
    #Clase utilizada como vista que redirecciona a login y presenta su template.
    login_url = 'login'
    model = ShippingAddress
    template_name = 'shipping_addresses/shipping_addresses.html'

    def get_queryset(self):
        #Función que filtra direcciones en base a cada usuario y su dirección por default.
        return ShippingAddress.objects.filter(user=self.request.user).order_by('-default')

class ShippingAdressUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    #Clase para actualizar una dirección.
    login_url = 'login'
    model = ShippingAddress
    form_class = ShippingAddressForm
    template_name = 'shipping_addresses/update.html'
    success_message = 'Address updated successfully'

    def get_success_url(self):
        #Función para regresar al template shipping_address si es exitosa.
        return reverse('shipping_addresses:shipping_addresses')

    def dispatch(self, request, *args, **kwargs):
        #Función para condicionar si el usuario es diferente retorna al carrito de compra, sino procede la petición.
        if request.user.id != self.get_object().user_id:
            return redirect('carts:cart')

        return super(ShippingAdressUpdateView, self).dispatch(request, *args, **kwargs)

class ShippingAdressDeleteView(LoginRequiredMixin, DeleteView):
    #Clase para eliminar una dirección.
    login_url = 'login'
    model = ShippingAddress
    template_name = 'shipping_addresses/delete.html'
    success_url = reverse_lazy('shipping_addresses:shipping_addresses')

    def dispatch(self, request, *args, **kwargs):
        #Función para eliminar la dirección tomando en cuenta si es default y si al usuario no le pertenece la misma.
        if self.get_object().default:
            return redirect('shipping_addresses:shipping_addresses')

        if request.user.id != self.get_object().user_id:
            return redirect('carts:cart')

        if self.get_object().has_orders():
            return redirect('shipping_addresses:shipping_addresses')

        return super(ShippingAdressDeleteView, self).dispatch(request, *args, **kwargs)

@login_required(login_url='login')
def create(request):
    #Función para crear una dirección tomando los valores ingresados por el usuario y guardandoos en la base de datos.
    form = ShippingAddressForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        shipping_address = form.save(commit=False)
        shipping_address.user = request.user
        shipping_address.default = not request.user.has_shipping_address()

        shipping_address.save()

        if request.GET.get('next'):
            if request.GET['next'] == reverse('orders:address'):
                cart = get_or_create_cart(request)
                order = get_or_create_order(cart, request)

                order.update_shipping_address(shipping_address)

                return HttpResponseRedirect(request.GET['next'])

        messages.success(request, 'Address created successfully')
        return redirect('shipping_addresses:shipping_addresses')

    return render(request, 'shipping_addresses/create.html', {
        'form' : form
    })

@login_required(login_url='login')
def default(request, pk):
    #Función para asignar una dirección por default a un usuario.
    shipping_address = get_object_or_404(ShippingAddress, pk=pk)

    if request.user.id != shipping_address.user_id:
        return redirect('carts:cart')

    if request.user.has_shipping_address():
        request.user.shipping_address.update_default()
        
    shipping_address.update_default(True)

    return redirect('shipping_addresses:shipping_addresses')
