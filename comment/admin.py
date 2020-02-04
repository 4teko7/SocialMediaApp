# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Comment
# Register your models here.

# admin.site.register(Article)
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["id","author","article","createdDate","comments2"]
    list_display_links = ["id","author","article"]
    search_fields = ["id","author","article"]
    list_filter = ["id","createdDate","author","article"]
    
    class Meta:
        model = Comment

