from django import template

register = template.Library()


@register.filter()
def title_contais(posts, texto=''):
    return (posts.filter(title__contains=texto))