from django import template

register = template.Library()


@register.filter(name='multiply')
def multiply(value, arg):
    if value is not None:
        return value * arg
    return None
