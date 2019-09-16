from django import template
from django.utils.safestring import mark_safe
from django.template import Library

import json
import numpy as np

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

@register.filter
def safe_js(value):
    if type(value) is np.ndarray:
        return mark_safe(json.dumps(value.tolist()))
    return mark_safe(json.dumps(value))