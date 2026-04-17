from django import template

register = template.Library()

@register.filter()
def clp(value):
    """
    Formatea un número como CLP (punto como miles, sin decimales).
    Ejemplo: 16000 -> 16.000
    """
    try:
        value = int(value)
        return f"{value:,}".replace(",", ".")
    except (ValueError, TypeError):
        return value
