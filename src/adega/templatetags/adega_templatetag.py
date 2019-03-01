from django import template

register = template.Library()

@register.filter
def to_percent(value):
    return "{:.2f}".format(float(value)*100) + "%"