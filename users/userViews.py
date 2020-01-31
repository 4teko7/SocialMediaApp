# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.hashers import make_password
from django.shortcuts import render,HttpResponse,redirect,HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from .userForms import *
from todo.models import Todo
from article.models import Article
from djangoBlog.language import *

# Create your views here.
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
# "allArticles":allArticles,"myTodos":myTodos,"myArticles":myArticles

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


def about(req):
    check(req)
    global context
    global lang
    context['lang'] = lang
    return render(req,"about.html",context)

def registerUser(req):
    form = registerForm()
    check(req)
    global context
    context['form'] = form
    global lang
    context['lang'] = lang  
    
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
            messages.success(req,lang['registered'])
            return redirect("mainPage")
        else:
            username = User.objects.filter(username = req.user.username)
            if(username):
                messages.warning(req,lang['usernameExists'])
            return render(req,"register.html",context)
    else:
        return render(req,"register.html",context)

   
def loginUser(req):
    form = loginForm()
    check(req)
    global context
    context['form'] = form
    global lang
    context['lang'] = lang  
    if(req.method == "POST"):
        form = loginForm(req.POST)
        if(form.is_valid()):
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            
            user = authenticate(username = username,password = password)
            if(user):
                messages.success(req,lang['loggedIn'])
                login(req,user)
                return redirect("mainPage")
            else:
                messages.info(req,lang['invalidUser'])
                return render(req,"login.html",context)
        else:
            return render(req,"login.html",context)

    else:
        return render(req,"login.html",context)


def logoutUser(req):
    logout(req)
    messages.success(req,lang['logoutMessage'])
    check(req)
    global context
    global lang
    context['lang'] = lang
    return render(req,"index.html",context)

def editProfile(req):
    user = User.objects.filter(username = req.user.username)
    form = ProfileForm(initial={'firstname': user[0].first_name,'lastname':user[0].last_name,'email':user[0].email})
    check(req)
    global context
    context['form'] = form
    global lang
    context['lang'] = lang
    return render(req,'editprofile.html',context)

def saveProfile(req):
    user = User.objects.get(username = req.user.username)
    form = ProfileForm(req.POST)
    if(form.is_valid()):
        user.first_name = form.cleaned_data.get("firstname")
        user.last_name = form.cleaned_data.get("lastname")
        user.email = form.cleaned_data.get("email")
        user.save()
        messages.success(req,lang['profileUpdated'])
        return HttpResponseRedirect("/users/about/")
    else:
        return HttpResponseRedirect('/users/editprofile/')


def changePassword(req):
    form = ChangePassword()
    check(req)
    global context
    context['form'] = form
    global lang
    context['lang'] = lang 
    if(req.method == "POST"):
        form = ChangePassword(req.POST)
        if(form.is_valid()):
            oldPassword = form.cleaned_data.get("oldPassword")
            newPassword = form.cleaned_data.get("newPassword")
            newPasswordConfirm = form.cleaned_data.get("newPasswordConfirm")
            user = User.objects.get(username = req.user.username)
            print(user.check_password(oldPassword))
            if(not user.check_password(oldPassword)):
                messages.warning(req,lang['oldPasswordIncorrect'])
                return HttpResponseRedirect('/users/changepassword/')
            elif(not (oldPassword or newPassword or newPasswordConfirm)):
                messages.warning(req,lang['fillFields'])
                return HttpResponseRedirect('/users/changepassword/')
            elif(newPassword != newPasswordConfirm):
                messages.warning(req,lang['newsdiff'])
                return HttpResponseRedirect('/users/changepassword/')
            else:
                user.set_password(newPassword)
                user.save()
                login(req,user)
                messages.warning(req,lang['passwordChanged'])
                return HttpResponseRedirect('/')
        else:
            messages.warning(req,lang['formInvalid'])
            return HttpResponseRedirect('/users/changepassword/')
    else:
        return render(req,"changepassword.html",context)


def changeUsername(req):
    form = ChangeUsername()
    check(req)
    global context
    context['form'] = form
    global lang
    context['lang'] = lang  
    if(req.method == "POST"):
        form = ChangeUsername(req.POST)
        if(form.is_valid()):
            newUsername = form.cleaned_data.get("newUsername")
            user = User.objects.filter(username = newUsername)

            if(user):
                messages.warning(req,lang['usernameExists'])
                form = ChangeUsername(initial = {'username':newUsername})
                context['form'] = form
                return render(req,'changeusername.html',context)

            else:
                req.user.username = newUsername
                req.user.save()
                messages.warning(req,lang['usernameChanged'])
                return HttpResponseRedirect('/')
        else:
            messages.warning(req,lang['formInvalid'])
            return HttpResponseRedirect('/users/changeusername/')
    else:
        return render(req,"changeusername.html",context)


def userLanguage(lang2):
    global lang
    global context
    lang = lang2
    context['lang'] = lang