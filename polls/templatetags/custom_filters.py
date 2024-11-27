from django import template
register = template.Library()

@register.filter
def get_item(dictionary, key):
    print('i will get the item' + dictionary.get(key, ''))
    return dictionary.get(key, '')