from random import sample

from django import template
from django.db.models import Count

from Main.models import Genre, Tag

register = template.Library()


@register.simple_tag()
def get_genres():
    return Genre.objects.all()


@register.simple_tag()
def get_tags():
    return Tag.objects.order_by('?')[:10]
