# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages

from .userForms import *
def about(req):
    context = {
        "name":"Bilal",
        "surname" : "Tekin",
        "numbers" : [1,2,3,4]
    }
    return render(req,"about.html",context)

def registerUser(req):
    form = registerForm()
    context = {
            "form" : form
             }
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
    context = {
        "form":loginForm()
    }
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
    return redirect("mainPage")
