
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import UserProfile

# Register your models here.

# admin.site.register(Article)
@admin.register(UserProfile)
class userAdmin(admin.ModelAdmin):
    list_display = ["profileImage"]
    # # list_display_links = []
    # # search_fields = []
    # # list_filter = []


    
    class Meta:
        model = UserProfile

