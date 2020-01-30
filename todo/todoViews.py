# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
from django.shortcuts import render,HttpResponse,redirect,HttpResponseRedirect,reverse
from .todoForms import *
from django.contrib import messages
from .models import Todo
# Create your views here.


def addTodo(req):
    form = addTodoForm()
    context = {
            "form" : form
             }
    if(req.method == "POST"):
        print("POSTA GIRDI")
        form = addTodoForm(req.POST)
        if(form.is_valid()):
            content = form.cleaned_data.get("content")
            date = form.cleaned_data.get("date")
            newTodo = Todo(content = content , date = date,author = req.user)
            newTodo.save()
            messages.success(req,"Todo is Successfully Added.")
            return HttpResponseRedirect('/todos/mytodos/')
        else:
            return render(req,"addtodo.html",context)
    else:
        return render(req,"addtodo.html",context)

def myTodos(req):
    todos = Todo.objects.filter(author = req.user)
    todos = todos.order_by('date')
    todos = todos.order_by('iscompleted')
    return render(req,"mytodos.html",{"todos":todos,"date":datetime.datetime.now()})

def completeTodo(req):
    id = req.POST.get('id')
    todo = Todo.objects.filter(id = id,author = req.user)
    if(todo):
        if(todo[0].iscompleted): todo[0].iscompleted = False
        else: todo[0].iscompleted = True
        todo[0].save()
        messages.success(req,"Todo is Successfully Completed.")
    return HttpResponseRedirect('/todos/mytodos/')