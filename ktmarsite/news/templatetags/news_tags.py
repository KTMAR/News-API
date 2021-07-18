from django import template
from django.template import Library
from news.models import *
from django.utils.html import mark_safe
register = template.Library()


@register.simple_tag(name='getcats')
def get_categories(filter=None):
    if not filter:
        return Category.objects.all()
    else:
        return Category.objects.filter(pk=filter)


@register.inclusion_tag('news/list_categories.html')
def show_categories(sort=None, cat_selected=0):
    if not sort:
        cats = Category.objects.all()
    else:
        cats = Category.objects.order_by(sort)

    return {'cats': cats, 'cat_selected': cat_selected}



@register.filter
def comments_filter(comments_list):
    res = """
        <ul>
        {}
        </ul>
        """
    i = ''
    for comment in comments_list:
        i +='''
            <li>
                {comment_id}
            </li>
        '''.format(comment_id=comment['id'])
        if comment.get('children'):
            i += comments_filter(comment['children'])

    return mark_safe(res.format(i))