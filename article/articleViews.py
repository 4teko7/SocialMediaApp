# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,HttpResponse,redirect,HttpResponseRedirect,render_to_response
from django.contrib import messages
from .articleForms import *
from .models import Article
from todo.models import Todo

context = {}
allArticles = 0
myTodos = 0
myArticles = 0
def allInfo(req):
    global allArticles
    global myTodos
    global myArticles
    allArticles = len(Article.objects.all())
    myTodos = len(Todo.objects.filter(author = req.user))
    myArticles = len(Article.objects.filter(author = req.user))
# "allArticles":allArticles,"myTodos":myTodos,"myArticles":myArticles

# Create your views here.
def index(req):
    # return HttpResponse("<h3>Anasayfa</h3>")
    check(req)
    return render(req,"index.html",context)

# def detail(req,id):
#     # return HttpResponse("<h3>Anasayfa</h3>")
#     check(req)
#     global context
#     context['id'] = id
#     return render(req,"index.html",context)



# Create your views here.


def addArticle(req):
    form = addArticleForm()
    check(req)
    global context
    context['form'] = form

    if(req.method == "POST"):
        form = addArticleForm(req.POST)
        if(form.is_valid()):
            article = form.save(commit = False)
            article.author = req.user
            article.save()
            messages.success(req,"Article Successfully Added.")
            return HttpResponseRedirect("/articles/myarticles/")
        else:

            return render(req,"addArticle.html",context)
    else:
        return render(req,"addArticle.html",context)


def myArticles(req):
    check(req)
    articles = Article.objects.filter(author = req.user)
    articles = articles.order_by("createdDate")
    global context
    context['articles'] = articles
    return render(req,"myarticles.html",context)


def articleDetail(req,id):
    check(req)
    article = Article.objects.filter(id = id)
    global context
    context['article'] = article[0]
    return render(req,"articledetail.html",context)
    # return HttpResponseRedirect('/articles/myarticles/')
def allArticles(req):
    articles = Article.objects.all()
    check(req)
    global context
    context['articles'] = articles
    
    return render(req,"allarticles.html",context)


def editArticle(req,id):
    check(req)

    articleOld = Article.objects.filter(id=id,author = req.user)
    form = addArticleForm(initial={'title': articleOld[0].title,'content':articleOld[0].content})
    global context
    context['form'] = form
    context['id'] = id

    if(req.method == "POST"):
 

        form = addArticleForm(req.POST)
        if(form.is_valid()):
            article = form.save(commit = False)
            article.id = articleOld[0].id
            article.createdDate = articleOld[0].createdDate
            article.author = req.user
            articleOld.delete()
            article.save()
            messages.success(req,"Article Successfully Added.")
            return HttpResponseRedirect("/articles/myarticles/")
        else:
            return render(req,"editarticle.html",context)
    else:

        if(articleOld):
            return render(req,"editarticle.html",context)
        else:
            return HttpResponseRedirect("/articles/myarticles/")

def deleteArticle(req,id):
    article = Article.objects.filter(id = id , author = req.user)
    if(article):
        article.delete()

    return HttpResponseRedirect('/articles/myarticles/')


def check(req):
    global context
    if(req.user.is_authenticated):
        allInfo(req)
        context = {
            "allArticles":allArticles,
            "myTodos":myTodos,
            "myArticles":myArticles
             }
    else:
        context = {}