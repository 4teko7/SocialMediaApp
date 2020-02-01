# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,HttpResponse,redirect,HttpResponseRedirect,render_to_response
from django.contrib import messages

from comment.commentForms import *
from article.models import *
from django.contrib.auth.decorators import login_required

# Create your views here.


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
def check(req):
    from .commentLang import lang2
    global context
    if(req.user.is_authenticated):
        allInfo(req)
        context = {
            "allArticles":allArticles,
            "myTodos":myTodos,
            "myArticles":myArticles,
            'lang':lang2
             }
    else:
        context = {"allArticles":allArticles,"lang":lang2}

@login_required(login_url="/users/login/")
def addComment(req,id):
    from .commentLang import lang2
    form = CommentForm()
    if(req.method == "POST"):
        form = CommentForm(req.POST)
        if(form.is_valid()):
            comment = form.save(commit = False)
            comment.author = req.user
            comment.article = Article.objects.filter(id = id)[0]
            articlee = comment.article
            comment.save()
            messages.success(req,lang2['commentAdded'])
            return HttpResponseRedirect("/articles/articledetail/"+id + "/")
        else:
            if(len(comment.content) > 4000):
                messages.success(req,lang['longComment'])
            return HttpResponseRedirect("/articles/articledetail/"+id + "/")
@login_required(login_url="/users/login/")
def addCommentComment(req,id):
    from .commentLang import lang2
    form = CommentForm(req.POST)
    articleId = req.POST.get("articleId")
    if(form.is_valid()):
        superComment = Comment.objects.get(id = id)
        content = form.cleaned_data.get("content")
        superComment.comments.append({"author":req.user.username,"content":content,"id":int(id)}) 
        superComment.save()
        messages.success(req,lang2['commentAdded'])
        return HttpResponseRedirect("/articles/articledetail/" + articleId + "/")
    else:
        messages.info(req,lang2['Comment is not Added'])
        return HttpResponseRedirect("/articles/articledetail/" + articleId + "/")

