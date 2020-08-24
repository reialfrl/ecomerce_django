from django import template

register = template.Library()

@register.filter()
def price_format(value):
    return 'S/{0:.2f}'.format(value)