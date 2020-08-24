from django.shortcuts import render
from django.shortcuts import redirect

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth import authenticate

from django.contrib.auth.models import User

from django.http import HttpResponseRedirect

from .forms import RegisterForm

from products.models import Product

def index(request):
    #Función para la vista index donde se muestran todos los productos.
    products = Product.objects.all().order_by('-id')

    return render(request, 'index.html', {
        'message': 'Products list',
        'title': 'Products',
        'products': products,
    })

def login_view(request):
    #Función para la vista de autentificación del usuario donde se hacen las verificaciones pertinentes.
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        username = request.POST.get('username') #DIC
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'Welcome {}'.format(user.username))

            if request.GET.get('next'):
                return HttpResponseRedirect(request.GET['next'])

            return redirect('index')
        else:
            messages.error(request, 'Incorrect Username or Password')

    return render(request, 'users/login.html', {

    })

def logout_view(request):
    #Función de la vista para registrar la salida de sesión de un usuario.
    logout(request)
    messages.success(request, 'Session closed successfully')
    return redirect('login')

def register(request):
    #Función con la que se verifica si el usuario esta ya autenticado y sino muestra el formulario de registro.
    if request.user.is_authenticated:
        return redirect('index')


    form = RegisterForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():

        user = form.save()
        if user:
            messages.success(request, 'User successfully created')
            return redirect('index')


    return render(request, 'users/register.html', {
        'form': form
    })
