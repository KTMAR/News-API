from django.core.cache import cache
from django.db.models import Count

from .models import *


class DataMixin:
    paginate_by = 3

    def get_user_context(self, **kwargs):
        context = kwargs
        cats = cache.get('cats')
        if not cats:
            cats = Category.objects.annotate(Count('news'))
            cache.set('cats', cats, 60)

        context['cats'] = cats
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context


def get_children(qs_child):
    res = []
    for comment in qs_child:
        c = {
            'id': comment.id,
            'text': comment.text,
            'timestamp': comment.timestamp.strftime('%Y-%m-%d %H:%m'),
            'author': comment.user,
            'is_child': comment.is_child,
            'parent_id': comment.get_parent,
        }
        if comment.comment_children.exists():
            c['children'] = get_children(comment.comment_children.all())
            res.append(c)
    return res


def create_comments_tree(qs):
    res = []
    for comment in qs:
        c = {
            'id': comment.id,
            'text': comment.text,
            'timestamp': comment.timestamp.strftime('%Y-%m-%d %H:%m'),
            'author': comment.user,
            'is_child': comment.is_child,
            'parent_id': comment.get_parent,
        }
        if comment.comment_children:
            c['children'] = get_children(comment.comment_children.all())
        if not comment.is_child:
            res.append(c)
    return res