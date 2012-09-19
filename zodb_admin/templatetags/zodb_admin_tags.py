from django import template

from ..models import Record

register = template.Library()


@register.filter
def zodb_create_urls(user):
    return Record.create_urls(user)
