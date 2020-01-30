from django.conf.urls import url
from django.contrib import admin
from article.articleViews import *
app_name = "articleroutes"

urlpatterns = [
    url("addarticle/",addArticle,name = "addarticle"),
    url("myarticles/",myArticles,name = "myarticles"),
    url("articledetail/(?P<id>\d+)/",articleDetail,name = "articledetail"),
    url("allarticles/",allArticles,name = "allarticles"),
    url("editarticle/(?P<id>\d+)/",editArticle,name = "editarticle"),
    url("deletearticle/(?P<id>\d+)/",deleteArticle,name = "deletearticle"),



]