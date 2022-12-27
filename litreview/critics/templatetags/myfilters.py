from django import template

register = template.Library()


@register.filter(name="stars")
def stars(number):
    return "&#9733;" * number
