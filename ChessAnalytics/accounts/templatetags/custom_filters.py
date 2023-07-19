from django import template
from datetime import date

register = template.Library()


@register.filter
def placeholder(value, token):
    value.field.widget.attrs['placeholder'] = token
    return value


@register.filter
def turn_birth_year_to_age(value):
    today = date.today()
    return (today - value).days // 365

