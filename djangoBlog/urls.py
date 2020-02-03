#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
from django.contrib.auth.models import User
from django.contrib import admin
from article.models import Article
from todo.models import Todo
from todo.todoLang import todoLanguage
from article.articleLang import articleLanguage
from users.userLang import userLanguage
from comment.commentLang import commentLanguage
from .language import *
import datetime
from users.models import UserProfile

from django.conf import settings
from django.conf.urls.static import static

context = {}
allArticles = 0
myTodos = 0
myArticles = 0
lang = en


def check(req):
    global context
    global allArticles
    if(req.user.is_authenticated):
        allInfo(req)
        context = {
            "allArticles":allArticles,
            "myTodos":myTodos,
            "myArticles":myArticles
             }
    else:
        allArticles = len(Article.objects.all())
        context = {"allArticles":allArticles}


def allInfo(req):
    global allArticles
    global myTodos
    global myArticles
    allArticles = len(Article.objects.all())
    myTodos = len(Todo.objects.filter(author = req.user))
    myArticles = len(Article.objects.filter(author = req.user))



def mainPage(req):
    global lang
    global context

    check(req)
    if(req.user.is_authenticated):
        articles = Article.objects.filter(author = req.user)
        articles = articles.order_by('id')
        articles = articles[::-1]
        articles = list(articles[:4])
        context['articles'] = articles


        todos = Todo.objects.filter(author = req.user)
        todos = todos.order_by('date')
        todos = list(filter(lambda x: not x.iscompleted, todos))
        todos = todos[:4]
        context['todos'] = todos

        profile = UserProfile.objects.filter(user = req.user)
        if(profile):
            if(profile[0].profileImage):
                context['profileImage'] = profile[0].profileImage
    context['date'] = datetime.datetime.now()
    context['lang'] = lang
    return render(req,"index.html",context)



def searchArticle(req):
    global context
    global lang
    check(req)
    context['lang'] = lang
    keywords = req.GET.get('keywords')
    if(keywords):
        articles = Article.objects.filter(title__contains = keywords)
        context['articles'] = articles
    return render(req,'allarticles.html',context)

def searchUser(req):
    global context
    global lang
    check(req)
    keywords = req.GET.get('keywords')
    context['lang'] = lang
    if(keywords):
        users = User.objects.filter(username__contains = keywords)

        context['users'] = users
    return render(req,'allusers.html',context)



def language(req):
    global lang
    global context
    if(lang['language'] == "ENGLISH"): lang = en
    else: lang = tr
    context['lang'] = lang

    todoLanguage(lang)
    articleLanguage(lang)
    userLanguage(lang)
    commentLanguage(lang)
    return redirect(req.GET.get("currentPage"))


urlpatterns = [
    url(r'admin/', admin.site.urls),
    url('users/', include("users.userRoutes")),
    url("articles/",include("article.articleRoutes")),
    url("todos/",include("todo.todoRoutes")),
    url('searchArticle/',searchArticle,name = 'searchArticle'),
    url('searchUser/',searchUser,name = "searchUser"),
    url('comments/',include('comment.commentRoutes')),
    url('language/',language,name = "language"),
    url('^$',mainPage,name = "mainPage"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)