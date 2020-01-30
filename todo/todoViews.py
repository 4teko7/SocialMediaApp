# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
from django.shortcuts import render,HttpResponse,redirect,HttpResponseRedirect,reverse
from .todoForms import *
from django.contrib import messages
from .models import Todo
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



def addTodo(req):
    form = addTodoForm()
    check(req)
    global context
    context['form'] = form
    allInfo(req)
    
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
    check(req)
    todos = Todo.objects.filter(author = req.user)
    todos = todos.order_by('date')
    todos = todos.order_by('iscompleted')
    global context
    context['todos'] = todos
    context['date'] = datetime.datetime.now()
    
    return render(req,"mytodos.html",context)

def completeTodo(req):
    id = req.POST.get('id')
    todo = Todo.objects.filter(id = id,author = req.user)
    if(todo):
        if(todo[0].iscompleted): todo[0].iscompleted = False
        else: todo[0].iscompleted = True
        todo[0].save()
        messages.success(req,"Todo is Successfully Completed.")
    return HttpResponseRedirect('/todos/mytodos/')


def deleteTodo(req,id):
    todo = Todo.objects.filter(id = id,author = req.user)
    todo.delete()
    return HttpResponseRedirect('/todos/mytodos/')


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