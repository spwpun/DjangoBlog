# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from blog.models import Article,Category,Tag
# Register your models here.
class ArticleAdmin(admin.ModelAdmin):
	list_display = ('title','abstract','pub_time')
	list_filter = ('modified_time',)

class CategoryAdmin(admin.ModelAdmin):
	list_display = ('name',)

class TagAdmin(admin.ModelAdmin):
	list_display = ('name',)

admin.site.register(Article,ArticleAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Tag,TagAdmin)