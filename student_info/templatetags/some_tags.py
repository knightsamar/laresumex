from django import template
from datetime import datetime

register = template.Library()

@register.filter
def split(str,splitter):
    if str is None:
        return []
    return str.split(splitter)
split.is_safe=True;

