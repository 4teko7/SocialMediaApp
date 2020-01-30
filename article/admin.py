# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Article
# Register your models here.

# admin.site.register(Article)
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ["id","title","author","createdDate"]
    list_display_links = ["title","createdDate"]
    search_fields = ["id","title"]
    list_filter = ["id","createdDate"]
    
    class Meta:
        model = Article

