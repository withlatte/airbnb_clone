from django import template

register = template.Library()


@register.filter
def ch_capitals(value):
    return value.capitalize()
