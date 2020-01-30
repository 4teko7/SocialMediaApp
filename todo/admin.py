# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Todo
# Register your models here.
@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ["title","author","createdDate"]
    list_display_links = ["title","createdDate"]
    search_fields = ["title"]
    list_filter = ["createdDate"]
    
    class Meta:
        model = Todo
