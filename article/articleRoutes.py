from django.conf.urls import url
from django.contrib import admin
from article.articleViews import *
app_name = "articleroutes"

urlpatterns = [
    url("detail/(?P<id>\d+)/",detail,name = "detail"),
]