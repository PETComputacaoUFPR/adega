from django import template

register = template.Library()

@register.filter
def to_percent(value):
    return "{:.2f}".format(float(value)*100) + "%"

@register.filter
def fix_2digit(value):
    return "{:.2f}".format(float(value))

@register.filter
def remove_spaces(value):
    return value.replace(' ', '')