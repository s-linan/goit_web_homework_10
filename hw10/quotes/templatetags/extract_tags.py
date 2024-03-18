from django import template


register = template.Library()


def tags(quotes_tag):
    return ', '.join([str(name) for name in quotes_tag.all()])


register.filter('tags', tags)

