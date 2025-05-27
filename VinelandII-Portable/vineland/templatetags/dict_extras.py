# templatetags/dict_extras.py
from django import template

register = template.Library()

@register.filter
def lookup(dictionary, key):
    """
    Permet d'accéder aux valeurs d'un dictionnaire avec une clé dynamique
    Usage: {{ dictionary|lookup:key }}
    """
    if dictionary is None:
        return None
    return dictionary.get(key, {})

@register.filter 
def get_item(dictionary, key):
    """
    Alternative pour accéder aux éléments d'un dictionnaire
    """
    if dictionary is None:
        return None
    return dictionary.get(key)

# Ajoutez ceci en haut de votre template HTML :
# {% load dict_extras %}