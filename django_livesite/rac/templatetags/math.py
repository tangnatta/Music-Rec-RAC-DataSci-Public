from django import template
from string import ascii_lowercase

register = template.Library()


@register.filter(name="time")
def t(value, arg):
    return value * int(arg)


@register.filter(name="round")
def r(value, arg):
    return round(value, int(arg))


@register.filter(name="hash")
def h(value, arg):
    hash_int = str(hash(value))[::-1][:int(arg)*2]
    hash_txt = ""
    for i in [hash_int[i:i+2] for i in range(0, len(hash_int), 2)]:
        hash_txt += ascii_lowercase[int(i) % 26]
    return hash_txt
