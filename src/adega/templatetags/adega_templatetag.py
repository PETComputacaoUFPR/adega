from django import template

register = template.Library()

@register.filter
def to_percent(value):
    if type(value) == int or type(value) == float:
        return "{:.2f}".format(float(value)*100) + "%"
    
    return ""
@register.filter
def fix_2digit(value):
    if type(value) == int or type(value) == float:
        return "{:.2f}".format(float(value))
    return ""

@register.filter
def remove_spaces(value):
    if type(value) == str:
        return value.replace(' ', '')
    return value