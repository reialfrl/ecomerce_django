from django import template

register = template.Library()

@register.filter()
def quantity_product_format(quantity=1):
    return '{} {}'.format(quantity, 'products' if quantity > 1 else 'product')


@register.filter()
def quantity_add_format(quantity=1):
    return '{} {}'.format(
        quantity_product_format(
            quantity), 'aggregates' if quantity > 1 else 'aggregate'
    )
    
