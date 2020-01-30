# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from .userForms import *

from todo.models import Todo
from article.models import Article
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
# "allArticles":allArticles,"myTodos":myTodos,"myArticles":myArticles




def about(req):
    check(req)
    global context
    return render(req,"about.html",context)

def registerUser(req):
    form = registerForm()
    check(req)
    global context
    context['form'] = form
      
    
    if(req.method == "POST"):
        print("POSTA GIRDI")
        form = registerForm(req.POST)
        if(form.is_valid()):
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            newUser = User(username = username)
            newUser.set_password(password)
            newUser.save()
            login(req,newUser)
            messages.success(req,"Successfully Registered.")
            return redirect("mainPage")
        else:
            return render(req,"register.html",context)
    else:
        return render(req,"register.html",context)

   
def loginUser(req):
    form = loginForm()
    check(req)
    global context
    context['form'] = form
      
    if(req.method == "POST"):
        form = loginForm(req.POST)
        if(form.is_valid()):
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            
            user = authenticate(username = username,password = password)
            if(user):
                messages.success(req,"Successfully Logged in to the Dashboard")
                login(req,user)
                return redirect("mainPage")
            else:
                messages.info(req,"Username or Password is invalid")
                return render(req,"login.html",context)
        else:
            return render(req,"login.html",context)

    else:
        return render(req,"login.html",context)
def logoutUser(req):
    logout(req)
    messages.success(req,"Logged Out Successfully")
    return render(req,"index.html")

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