from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def round_number(value):
    value = float(value)
    rounded_value = round(value, 1)
    return rounded_value

@register.filter
def released_year(val):
    return val[:4]

@register.filter(name='times')
def times(number):
    return range(1,number+1)

@register.filter
def published(pub):
    return pub[:10]