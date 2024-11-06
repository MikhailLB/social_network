from django import template
from django.db.models import Count

import humster.views as views
from humster.models import Category, tagPost
from humster.utils import menu

register = template.Library()

@register.inclusion_tag('humster/list_categories.html')
def show_categories(cat_selected=0):
    cats = Category.objects.annotate(total=Count("posts")).filter(total__gt=0)
    return {'cats': cats, 'cat_selected': cat_selected}

@register.inclusion_tag('humster/list_tags.html')
def show_all_tags():
    return {'tags': tagPost.objects.annotate(total=Count("tags")).filter(total__gt=0)}

@register.simple_tag
def get_menu():
    return menu