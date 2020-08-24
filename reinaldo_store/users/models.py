from stripeAPI.customer import create_customer

from django.db import models

from django.contrib.auth.models import AbstractUser

from orders.common import OrderStatus

class User(AbstractUser):
    #Clase para el modelo User con diferentes funciones y propiedades que seran utilizados en otros modelos.

    customer_id = models.CharField(max_length=100, blank=True, null=True)

    def get_full_name(self):
        #Obtener el nombre completo del usuario.
        return '{} {}'.format(self.first_name, self.last_name)

    def has_billing_profiles(self):
        #Retornar los metodos de pagos existentes.
        return self.billingprofile_set.exists()
    
    def has_customer(self):
        #Retornar el customer_id si no es None.
        return self.customer_id is not None

    def create_customer_id(self):
        #Si el customer_id no esta creado, con esta función lo hacemos.
        if not self.has_customer():
            customer = create_customer(self)
            self.customer_id = customer.id
            self.save()

    def has_shipping_address(self):
        #Retornar shipping_address si no es None.
        return self.shipping_address is not None

    def orders_completed(self):
        #Retornar solo las ordenes completadas, ordenandose por el id de forma descendente.
        return self.order_set.filter(status=OrderStatus.COMPLETED).order_by('-id')

    def has_shipping_addresses(self):
        #Retornar todas las shipping_address existentes.
        return self.shippingaddress_set.exists()

    def billing_profiles(self):
        #Retornar billing_profile existentes que sean unicamente default de forma descendente.
        return self.billingprofile_set.all().order_by('-default')

    @property
    def shipping_address(self):
        #Propiedad en donde solo se filtran las shipping_address que sean default.
        return self.shippingaddress_set.filter(default=True).first()

    @property
    def billing_profile(self):
        #Propiedad en donde solo se filtran las billing_profile que sean default.
        return self.billingprofile_set.filter(default=True).first()

    @property
    def description(self):
        #Propiedad donde se muestra una descripcion de un usuario.
        return 'Description for user {}'.format(self.username)

    @property
        #Propiedad con la que se retornan todas las shipping_address.
    def addresses(self):
        return self.shippingaddress_set.all()

class Customer(User):

    class Meta:
        proxy = True

    def get_products(self):
        return []

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
