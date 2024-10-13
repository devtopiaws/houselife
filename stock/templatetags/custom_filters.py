from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Obtiene el valor de un diccionario por la clave."""
    return dictionary.get(key)