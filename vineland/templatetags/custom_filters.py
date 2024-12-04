from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """
    Filtre pour accéder aux éléments d'un dictionnaire
    Usage: {{ dictionary|get_item:key }}
    """
    return dictionary.get(key)

@register.filter
def split_notes(notes_text):
    """
    Filtre pour diviser les notes en liste
    Usage: {{ question.note|split_notes }}
    """
    if not notes_text:
        return []
    return [note.strip() for note in notes_text.split('|')]

@register.filter
def format_age_range(plage):
    """
    Filtre pour formater la plage d'âge
    Usage: {{ plage|format_age_range }}
    """
    if not plage:
        return ""
    if plage.age_fin:
        return f"{plage.age_debut}-{plage.age_fin} ans"
    return f"{plage.age_debut}+ ans"

@register.filter
def multiply(value, arg):
    return value * arg

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def items(dictionary):
    if dictionary:
        return dictionary.items()
    return []