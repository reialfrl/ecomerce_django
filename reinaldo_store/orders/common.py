from enum import Enum

class OrderStatus(Enum):
    #Clase para verificar el status de la orden
    CREATED = 'CREATED'
    PAYED = 'PAYED'
    COMPLETED = 'COMPLETED'
    CANCELED = 'CANCELED'

choices = [(tag, tag.value) for tag in OrderStatus]
