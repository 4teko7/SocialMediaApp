# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,HttpResponse,redirect
from .todoForms import *
from django.contrib import messages

# Create your views here.


def addTodo(req):
    form = addTodoForm(req.POST or None)
    context = {
            "form" : form
             }
    
    if(form.is_valid()):
        todo = form.save(commit = False)
        todo.author = req.user
        todo.save()
        messages.success(req,"Todo Successfully Added.")
        return redirect("mainPage")
    else:
        return render(req,"addtodo.html",context)
