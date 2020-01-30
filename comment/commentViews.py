# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,HttpResponse,redirect,HttpResponseRedirect,render_to_response
from django.contrib import messages

from comment.commentForms import *
from article.models import *

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

def addComment(req,id):
    form = CommentForm()
    if(req.method == "POST"):
        form = CommentForm(req.POST)
        if(form.is_valid()):
            comment = form.save(commit = False)
            comment.author = req.user
            comment.article = Article.objects.filter(id = id)[0]
            comment.save()
            messages.success(req,"Comment Successfully Added.")
            return HttpResponseRedirect("/articles/articledetail/"+id + "/")
        else:

            return HttpResponseRedirect("/articles/articledetail/"+id + "/")

