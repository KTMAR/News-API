from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.utils.safestring import mark_safe

from .models import *


class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'cat', 'time_created', 'time_updated', 'is_published', 'get_html_photo',
                    'owner_name', 'author_name'
                    )
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'cat')
    prepopulated_fields = {'slug': ('title',)}
    fields = ('title', 'slug', 'cat', 'content', 'photo', 'get_html_photo', 'is_published', 'time_created',
              'time_updated', 'owner_name',)
    readonly_fields = ('time_created', 'time_updated', 'get_html_photo')

    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}'width=50>")

    get_html_photo.short_description = 'Изображение-миниатюра'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(News, NewsAdmin)
admin.site.register(Category, CategoryAdmin)

@admin.register(UserNewsRelation)
class UserNewsRelationAdmin(ModelAdmin):
    pass

# admin.site.register(Comments)

admin.site.site_title = 'Админка Криптовалютчика'
admin.site.site_header = 'Админка Криптовалютчика'
