from . import stripe

def create_customer(user):
    #Funcion con la que se puede obtener información relevante del cliente.
    customer = stripe.Customer.create(
        description=user.description 
    )

    return customer