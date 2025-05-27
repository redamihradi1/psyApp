from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Permet d'accéder à un élément de dictionnaire avec une clé dynamique dans un template"""
    if dictionary is None:
        return None
    return dictionary.get(key)

@register.filter
def is_before(sd1, sd2):
    """Vérifie si sd1 vient avant sd2 dans l'ordre lexicographique"""
    return sd1 < sd2

@register.filter
def multiply(value, arg):
    """Multiplie value par arg"""
    try:
        return int(value) * int(arg)
    except (ValueError, TypeError):
        return value

@register.filter
def add(value, arg):
    """Concatène deux chaînes"""
    return str(value) + str(arg)