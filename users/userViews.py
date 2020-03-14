# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.hashers import make_password
from django.shortcuts import render,HttpResponse,redirect,HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from .userForms import *
from .models import UserProfile
from todo.models import Todo
from article.models import Article
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
    allArticles = len(Article.objects.filter(isPrivate = False))
    myTodos = len(Todo.objects.filter(author = req.user))
    myArticles = len(Article.objects.filter(author = req.user))
# "allArticles":allArticles,"myTodos":myTodos,"myArticles":myArticles

def check(req):
    
    from .userLang import lang2
    global allArticles
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
        context = {"allArticles":allArticles,"lang":lang2}

@login_required(login_url="/users/login/")
def about(req):
    check(req)
    global context
    profile = UserProfile.objects.filter(user = req.user)
    if(profile):
        if(profile[0].profileImage):
            context['profileImage'] = profile[0].profileImage
    return render(req,"about.html",context)

def registerUser(req):
    from .userLang import lang2

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
            messages.success(req,lang2['registered'])
            return redirect("mainPage")
        else:
            username = User.objects.filter(username = req.user.username)
            if(username):
                messages.warning(req,lang2['usernameExists'])
            return render(req,"register.html",context)
    else:
        return render(req,"register.html",context)


def loginUser(req):
    from .userLang import lang2

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
                messages.success(req,lang2['loggedIn'])
                login(req,user)
                return redirect("mainPage")
            else:
                messages.info(req,lang2['invalidUser'])
                return render(req,"login.html",context)
        else:
            return render(req,"login.html",context)

    else:
        return render(req,"login.html",context)


def logoutUser(req):
    from .userLang import lang2

    logout(req)
    messages.success(req,lang2['logoutMessage'])
    check(req)
    global context
    return render(req,"index.html",context)

@login_required(login_url="/users/login/")
def editProfile(req):

    user = User.objects.filter(username = req.user.username)
    form = ProfileForm(initial={'firstname': user[0].first_name,'lastname':user[0].last_name,'email':user[0].email})
    check(req)
    global context
    context['form'] = form
    return render(req,'editprofile.html',context)

@login_required(login_url="/users/login/")
def saveProfile(req):
    from .userLang import lang2

    user = User.objects.get(username = req.user.username)
    form = ProfileForm(req.POST)
    if(form.is_valid()):
        user.first_name = form.cleaned_data.get("firstname")
        user.last_name = form.cleaned_data.get("lastname")
        user.email = form.cleaned_data.get("email")
        user.save()
        messages.success(req,lang2['profileUpdated'])
        return HttpResponseRedirect("/users/about/")
    else:
        return HttpResponseRedirect('/users/editprofile/')

def addProfileImage(req):
    from .userLang import lang2
    check(req)
    global context
    profile = UserProfile.objects.filter(user=req.user)

    if(req.method == "POST"):
        form = addProfileImageForm(req.POST,req.FILES or None)
        if(form.is_valid()):
            if(form.cleaned_data.get("profileImage")):
                if(UserProfile.objects.count() > 0):
                    profile.delete()
                profile = form.save(commit = False)
                profile.user = req.user
                profile.profileImage = form.cleaned_data.get("profileImage")
                profile.save()
            else:
                print("SILMEYE GELDI")
                if(req.POST.get("profileImage-clear")):
                    print("SILMEYE GELDI ICERIDE")
                    if(profile):
                        if(profile[0].profileImage):
                            profile[0].profileImage = None
                            profile[0].save()
            # article.author = req.user

            messages.success(req,lang2['articleAdded'])
            return HttpResponseRedirect("/users/about/")
        else:

            return render(req,"addprofileimage.html",context)
    else:
        form = addProfileImageForm()
        if(profile):
            if(profile[0].profileImage):
                context['profileImage'] = profile[0].profileImage
                form = addProfileImageForm(initial={'profileImage': profile[0].profileImage})
        context['form'] = form
        return render(req,"addprofileimage.html",context)

@login_required(login_url="/users/login/")
def changePassword(req):
    from .userLang import lang2

    form = ChangePassword()
    check(req)
    global context
    context['form'] = form
    if(req.method == "POST"):
        form = ChangePassword(req.POST)
        if(form.is_valid()):
            oldPassword = form.cleaned_data.get("oldPassword")
            newPassword = form.cleaned_data.get("newPassword")
            newPasswordConfirm = form.cleaned_data.get("newPasswordConfirm")
            user = User.objects.get(username = req.user.username)
            print(user.check_password(oldPassword))
            if(not user.check_password(oldPassword)):
                messages.warning(req,lang2['oldPasswordIncorrect'])
                return HttpResponseRedirect('/users/changepassword/')
            elif(not (oldPassword or newPassword or newPasswordConfirm)):
                messages.warning(req,lang2['fillFields'])
                return HttpResponseRedirect('/users/changepassword/')
            elif(newPassword != newPasswordConfirm):
                messages.warning(req,lang2['newsdiff'])
                return HttpResponseRedirect('/users/changepassword/')
            else:
                user.set_password(newPassword)
                user.save()
                login(req,user)
                messages.warning(req,lang2['passwordChanged'])
                return HttpResponseRedirect('/')
        else:
            messages.warning(req,lang2['formInvalid'])
            return HttpResponseRedirect('/users/changepassword/')
    else:
        return render(req,"changepassword.html",context)


@login_required(login_url="/users/login/")
def changeUsername(req):
    from .userLang import lang2

    form = ChangeUsername()
    check(req)
    global context
    context['form'] = form
    if(req.method == "POST"):
        form = ChangeUsername(req.POST)
        if(form.is_valid()):
            newUsername = form.cleaned_data.get("newUsername")
            user = User.objects.filter(username = newUsername)

            if(user):
                messages.warning(req,lang2['usernameExists'])
                form = ChangeUsername(initial = {'username':newUsername})
                context['form'] = form
                return render(req,'changeusername.html',context)

            else:
                req.user.username = newUsername
                req.user.save()
                messages.warning(req,lang2['usernameChanged'])
                return HttpResponseRedirect('/')
        else:
            messages.warning(req,lang2['formInvalid'])
            return HttpResponseRedirect('/users/changeusername/')
    else:
        return render(req,"changeusername.html",context)


def profile(req,id):
    check(req)
    user = User.objects.get(id = id)
    context['user'] = user
    profile = UserProfile.objects.filter(user = user)
    if(profile):
        if(profile[0].profileImage):
            context['profileImage'] = profile[0].profileImage
    return render(req,'profile.html',context)


