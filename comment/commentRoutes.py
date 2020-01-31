from django.conf.urls import url
from django.contrib import admin
from .commentViews import *
app_name = "commentroutes"

urlpatterns = [
    url("addcomment/(?P<id>\d+)/",addComment,name="addcomment"),
    url("addcommentcomment/(?P<id>\d+)/",addCommentComment,name="addcommentcomment"),
]
