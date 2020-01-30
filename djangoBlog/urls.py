"""djangoBlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from __future__ import unicode_literals
from django.conf.urls import url,include
from django.shortcuts import render,HttpResponse,redirect
from django.contrib import admin
from article.models import Article
from todo.models import Todo


def mainPage(req):
    if(req.user.is_authenticated):
        allArticles = len(Article.objects.all())
        myTodos = len(Todo.objects.filter(author = req.user))
        myArticles = len(Article.objects.filter(author = req.user))

        context = {
            "allArticles":allArticles,
            "myTodos":myTodos,
            "myArticles":myArticles
        }
    else:
        context = {}
    return render(req,"index.html",context)
    
urlpatterns = [
    url(r'admin/', admin.site.urls),
    url('users/', include("users.userRoutes")),
    url("articles/",include("article.articleRoutes")),
    url("todos/",include("todo.todoRoutes")),
    url("",mainPage,name="mainPage")
]

