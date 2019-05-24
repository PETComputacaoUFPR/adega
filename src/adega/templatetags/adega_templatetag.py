from django import template

register = template.Library()

@register.filter
def to_percent(value):
    try:
        return "{:.2f}".format(float(value)*100) + "%"
    except:
        return ""

@register.filter
def fix_2digit(value):
    try:
        return "{:.2f}".format(float(value))
    except e:
        return ""

@register.filter
def remove_spaces(value):
    try:
        return value.replace(' ', '')
    except:
        return value