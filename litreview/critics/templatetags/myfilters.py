from django import template

register = template.Library()


@register.filter(name="stars")
def stars(number):
    string = "&#9733;" * number
    while number < 5:
        string += "&#9734"
        number += 1
    return string
