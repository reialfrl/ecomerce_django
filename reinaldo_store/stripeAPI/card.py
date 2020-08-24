from . import stripe

def create_card(user, token):
    #función creada en base a la documentacion de stripe para crear una nueva tarjeta.
    source = stripe.Customer.create_source(
        user.customer_id,
        source=token,
    )

    return source