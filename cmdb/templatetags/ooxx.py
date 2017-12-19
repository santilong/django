#Author:Santi
from django import template

register = template.Library()

@register.simple_tag()
def hello(a1,a2):
    return a1 + a2

@register.filter()
def world(a1,a2):
    return a1 + a2