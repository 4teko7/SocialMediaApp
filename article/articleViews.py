# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,HttpResponse,redirect,HttpResponseRedirect,render_to_response,get_object_or_404
from django.contrib import messages
from .articleForms import *
from .models import Article
from todo.models import Todo
from comment.models import Comment
from comment.commentForms import *
from django.contrib.auth.decorators import login_required
contex = {}


allArticles = 0
myTodos = 0
myArticles = 0

def allInfo(req):
    global allArticles
    global myTodos
    global myArticles
    allArticles = len(Article.objects.filter(isPrivate = False))
    myTodos = len(Todo.objects.filter(author = req.user))
    myArticles = len(Article.objects.filter(author = req.user))


def check(req):
    from .articleLang import lang2
    global context
    if(req.user.is_authenticated):
        allInfo(req)
        context = {
            "allArticles":allArticles,
            "myTodos":myTodos,
            "myArticles":myArticles,
            "lang":lang2
             }
    else:
        global allArticles
        allArticles = len(Article.objects.all())
        context = {"allArticles":allArticles,
                    "lang":lang2
            }
# "allArticles":allArticles,"myTodos":myTodos,"myArticles":myArticles

# Create your views here.



# Create your views here.

@login_required(login_url="/users/login/")
def addArticle(req):
    from .articleLang import lang2
    form = addArticleForm()
    check(req)
    global context
    context['form'] = form
    if(req.method == "POST"):
        form = addArticleForm(req.POST,req.FILES or None)
        print(req.FILES)
        if(form.is_valid()):
            article = form.save(commit = False)
            article.author = req.user
            article.save()
            print("ARTICLE IMG : ",article.articleImage)
            messages.success(req,lang2['articleAdded'])
            return HttpResponseRedirect("/articles/myarticles/")
        else:

            return render(req,"addArticle.html",context)
    else:
        return render(req,"addArticle.html",context)

@login_required(login_url="/users/login/")
def myArticles(req):
    check(req)
    articles = Article.objects.filter(author = req.user)
    articles = articles.order_by("createdDate")
    global context
    context['articles'] = articles
    return render(req,"myarticles.html",context)

def articleDetail(req,id):
    commentForm = CommentForm()
    check(req)
    article = Article.objects.filter(id = id)
    if(not article):
        return render(req,"warnings/pagenotfound.html",context)
    comments = Comment.objects.filter(article = article)
    commets = comments.order_by('createdDate')
    comments = comments[::-1]
    global context
    context['article'] = article[0]
    context['commentForm'] = commentForm
    context['comments'] = comments
    if(article[0].articleImage):
        context["image"] = article[0].articleImage.url
        print(context['image'])
    if(article[0].isPrivate):
        if(article[0].author == req.user):
            return render(req,"articledetail.html",context)
        else:
            return render(req,"warnings/articleprivate.html",context)
    else:
        return render(req,"articledetail.html",context)

    # return HttpResponseRedirect('/articles/myarticles/')

def allArticles(req):
    articles = Article.objects.all()
    check(req)
    global context
    context['articles'] = articles
    return render(req,"allarticles.html",context)

@login_required(login_url="/users/login/")
def editArticle(req,id):
    from .articleLang import lang2

    check(req)

    articleOld = Article.objects.filter(id=id,author = req.user)
    if(not articleOld):
        return render(req,"warnings/canteditarticle.html",context)

    form = addArticleForm(initial={'title': articleOld[0].title,'content':articleOld[0].content,'isPrivate':articleOld[0].isPrivate,'articleImage':articleOld[0].articleImage})
    global context
    context['form'] = form
    context['id'] = id
    if(req.method == "POST"):
        

        form = addArticleForm(req.POST,req.FILES)
        if(form.is_valid()):
            article = form.save(commit = False)
            article.id = articleOld[0].id
            article.createdDate = articleOld[0].createdDate
            article.author = req.user
            articleOld.delete()
            article.save()
            messages.success(req,lang2['articleUpdated'])
            return HttpResponseRedirect("/articles/myarticles/")
        else:
            return render(req,"editarticle.html",context)
    else:

        if(articleOld):
            if(articleOld[0].isPrivate):
                if(articleOld[0].author == req.user):
                    return render(req,"editarticle.html",context)
                else:
                    return render(req,"warnings/articleprivate.html",context)
            else:
                return render(req,"editarticle.html",context)

@login_required(login_url="/users/login/")
def deleteArticle(req,id):
    from .articleLang import lang2
    article = Article.objects.filter(id = id , author = req.user)
    if(not article):
        return render(req,"warnings/pagenotfound.html",context)
    else:
        article.delete()
        messages.success(req,lang2['articleDeleted'])
        return HttpResponseRedirect('/articles/myarticles/')



    
