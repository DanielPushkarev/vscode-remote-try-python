from django import template

register = template.Library()

bad_words = ['дурак', 'Дура']

@register.filter()
def censor(value):
    if not isinstance(value, str):
        raise TypeError()

    for word in bad_words:
        value = value.replace(word, word[0] + '*' * (len(word) - 1))
    return value