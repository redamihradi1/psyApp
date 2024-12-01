from django import template

register = template.Library()

@register.filter
def split(value, separator='|'):
    """
    Divise une chaîne de caractères selon un séparateur.
    Usage: {{ value|split:'|' }}
    """
    return value.split(separator)