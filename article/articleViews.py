# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,HttpResponse,redirect,HttpResponseRedirect,render_to_response
from django.contrib import messages
from .articleForms import *
from .models import Article

# Create your views here.
def index(req):
    # return HttpResponse("<h3>Anasayfa</h3>")
    return render(req,"index.html",{"a":"Bilal"})

def detail(req,id):
    # return HttpResponse("<h3>Anasayfa</h3>")
    context = {
        "id":id
    }
    return render(req,"index.html",context)



# Create your views here.


def addArticle(req):

    form = addArticleForm()
    context = {
            "form" : form
             }
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
    articles = Article.objects.filter(author = req.user)
    articles = articles.order_by("createdDate")
    return render(req,"myarticles.html",{"articles":articles})


def articleDetail(req,id):
    article = Article.objects.filter(id = id)
    
    return render(req,"articledetail.html",{"article":article[0]})
    # return HttpResponseRedirect('/articles/myarticles/')
def allArticles(req):
    articles = Article.objects.all()
    return render(req,"allarticles.html",{"articles":articles})


def editArticle(req,id):
    articleOld = Article.objects.filter(id=id,author = req.user)

    form = addArticleForm(initial={'title': articleOld[0].title,'content':articleOld[0].content})
    context = {
            "form" : form,
            "id":id
             }
    if(req.method == "POST"):
        print("POST Girdi.@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@2222222222222")

        form = addArticleForm(req.POST)
        if(form.is_valid()):
            article = form.save(commit = False)
            # articleOld[0].title = article.title
            # articleOld[0].content = article.content
            # articleOld[0].save()
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
        # form["title"] = articleOld[0].title
        # form["content"] = articleOld[0].content
        print("GET Girdi.@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@2222222222222")

        if(articleOld):
            return render(req,"editarticle.html",context)
        else:
            return HttpResponseRedirect("/articles/myarticles/")

def deleteArticle(req,id):
    article = Article.objects.filter(id = id , author = req.user)
    if(article):
        article.delete()

    return HttpResponseRedirect('/articles/myarticles/')
