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
from django.contrib.auth.models import User
from users.models import UserProfile
import json

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
    global allArticles
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
        allArticles = len(Article.objects.filter(isPrivate = False))
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
    parsed = []
    global context
    commentForm = CommentForm()
    check(req)
    article = Article.objects.filter(id = id)
    
    if(not article):
        return render(req,"warnings/pagenotfound.html",context)
    comments = Comment.objects.filter(article = article)
    comments = comments.order_by('createdDate')
    comments = comments[::-1]
    context['article'] = article[0]
    context['commentForm'] = commentForm



    for comment in comments:
        if(comment.comments2):
           
            parsed = json.loads(comment.comments2)
            for com in parsed:
                user = User.objects.get(username = com["author"])
                profile = UserProfile.objects.filter(user = user)
                if(profile):
                    if(profile[0].profileImage):
                        com["userImage"] = profile[0].profileImage.url
                    else:
                        com["userImage"] = None
                    comment.comments2 = parsed
        user = User.objects.get(username = comment.author)
        profile = UserProfile.objects.filter(user = user)
        if(profile):
            if(profile[0].profileImage):
                comment.userImage = profile[0].profileImage.url
            else:
                comment.userImage = None


       

    context['comments'] = comments
    if(article[0].articleImage):
        context["image"] = article[0].articleImage.url
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
    global context
    from .articleLang import lang2

    check(req)

    articleOld = Article.objects.filter(id=id,author = req.user)
    if(not articleOld):
        return render(req,"warnings/canteditarticle.html",context)

    form = addArticleForm(initial={'title': articleOld[0].title,'content':articleOld[0].content,'isPrivate':articleOld[0].isPrivate,'articleImage':articleOld[0].articleImage})
    context['form'] = form
    context['id'] = id
    if(req.method == "POST"):
        
        form = addArticleForm(req.POST,req.FILES)
        if(form.is_valid()):
            articleOld[0].content = form.cleaned_data.get("content")
            articleOld[0].title = form.cleaned_data.get("title")
            if(form.cleaned_data.get("articleImage")):
                articleOld[0].articleImage = form.cleaned_data.get("articleImage")
            else:
                if(req.POST.get("articleImage-clear")):
                    articleOld[0].articleImage = None
                
            articleOld[0].save()
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



    
