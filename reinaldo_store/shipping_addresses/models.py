from django.db import models

from users.models import User

class ShippingAddress(models.Model):
    #Clase con la que se crea todo el formulario de shipping_address
    user = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    line1 = models.CharField(max_length=200)
    line2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=50)
    reference = models.CharField(max_length=300)
    postal_code = models.CharField(max_length=10)
    default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.postal_code

    def has_orders(self):
        #Retorna el valor de la orden cuando es mayor o igual a 1.
        return self.order_set.count() >= 1

    def update_default(self, default=False):
        #Se actualiza el valor por default a True.
        self.default = default
        self.save()
    
    @property
    def address(self):
        #Propiedad con la que se retorna la dirección con su ciudad, estado y pais.
        return '{} - {} - {}'.format(self.city, self.state, self.country)