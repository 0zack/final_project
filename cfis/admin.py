from django.contrib import admin

from cfis.models import News, Post, Category, Tag

admin.site.register(News)
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Tag)