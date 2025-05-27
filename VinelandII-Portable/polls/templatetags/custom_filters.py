from django import template
register = template.Library()

@register.filter
def get_item(dictionary, key):
    print('i will get the item' + dictionary.get(key, ''))
    return dictionary.get(key, '')

@register.filter
def filter_by_domain(resultat_final, domain):
    """Compte le nombre d'éléments pour un domaine donné"""
    return [item for item in resultat_final if item['domaine'] == domain]

@register.filter
def concat(value, arg):
    return f"{value}{arg}"