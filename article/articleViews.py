# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,HttpResponse,redirect,HttpResponseRedirect,render_to_response
from django.contrib import messages
from .articleForms import *
from .models import Article
from todo.models import Todo
from comment.models import Comment
from comment.commentForms import *
from djangoBlog.language import *

context = {}
allArticles = 0
myTodos = 0
myArticles = 0
lang = en

def allInfo(req):
    global allArticles
    global myTodos
    global myArticles
    allArticles = len(Article.objects.all())
    myTodos = len(Todo.objects.filter(author = req.user))
    myArticles = len(Article.objects.filter(author = req.user))


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
        global allArticles
        allArticles = len(Article.objects.all())
        context = {"allArticles":allArticles}
# "allArticles":allArticles,"myTodos":myTodos,"myArticles":myArticles

# Create your views here.



# Create your views here.


def addArticle(req):
    form = addArticleForm()
    check(req)
    global context
    context['form'] = form
    global lang
    context['lang'] = lang
    if(req.method == "POST"):
        form = addArticleForm(req.POST)
        if(form.is_valid()):
            article = form.save(commit = False)
            article.author = req.user
            article.save()
            messages.success(req,lang['articleAdded'])
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
    global lang
    context['lang'] = lang
    return render(req,"myarticles.html",context)


def articleDetail(req,id):
    commentForm = CommentForm()
    check(req)
    article = Article.objects.filter(id = id)
    comments = Comment.objects.filter(article = article)
    commets = comments.order_by('createdDate')
    comments = comments[::-1]
    global context
    context['article'] = article[0]
    context['commentForm'] = commentForm
    context['comments'] = comments
    global lang
    context['lang'] = lang
    return render(req,"articledetail.html",context)
    # return HttpResponseRedirect('/articles/myarticles/')


def allArticles(req):
    articles = Article.objects.all()
    check(req)
    global context
    context['articles'] = articles
    global lang
    context['lang'] = lang
    return render(req,"allarticles.html",context)


def editArticle(req,id):
    check(req)

    articleOld = Article.objects.filter(id=id,author = req.user)
    form = addArticleForm(initial={'title': articleOld[0].title,'content':articleOld[0].content})
    global context
    context['form'] = form
    context['id'] = id
    global lang
    context['lang'] = lang
    if(req.method == "POST"):
 

        form = addArticleForm(req.POST)
        if(form.is_valid()):
            article = form.save(commit = False)
            article.id = articleOld[0].id
            article.createdDate = articleOld[0].createdDate
            article.author = req.user
            articleOld.delete()
            article.save()
            messages.success(req,lang['articleUpdated'])
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
        messages.success(req,lang['articleDeleted'])

    return HttpResponseRedirect('/articles/myarticles/')


def articleLanguage(lang2):
    global lang
    global context
    lang = lang2
    context['lang'] = lang


    
