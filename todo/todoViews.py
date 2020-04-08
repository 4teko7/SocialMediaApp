# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
from django.shortcuts import render,HttpResponse,redirect,HttpResponseRedirect,reverse
from .todoForms import *
from django.contrib import messages
from .models import Todo
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
    global allArticles

    from .todoLang import lang2
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
def addTodo(req):
    from .todoLang import lang2
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
            date = req.POST.get("date")
            newTodo = Todo(content = content , date = date,author = req.user)
            newTodo.save()
            messages.success(req,lang2['todoAdded'])
            return HttpResponseRedirect('/todos/mytodos/')
        else:
            return render(req,"addtodo.html",context)
    else:
        return render(req,"addtodo.html",context)



@login_required(login_url="/users/login/")
def editTodo(req,id):
    from .todoLang import lang2
    todo = Todo.objects.get(id = id)
    if(req.method == "POST"):
        form = addTodoForm(req.POST)
        if(form.is_valid()):
            content = form.cleaned_data.get("content")
            date = req.POST.get("date")
            todo.content = content
            todo.date = date
            todo.save()
            messages.success(req,lang2['todoAdded'])
            return HttpResponseRedirect('/todos/mytodos/')
        else:
            return HttpResponseRedirect('/todos/mytodos/')
    else:
        return HttpResponseRedirect('/todos/mytodos/')



@login_required(login_url="/users/login/")
def myTodos(req):

    form = addTodoForm()



    check(req)
    todos = Todo.objects.filter(author = req.user)
    todos = todos.order_by('date')
    todos = list(filter(lambda x: not x.iscompleted, todos))
    for todo in todos:
        print(todo.date)

    todosCompleted = Todo.objects.filter(author = req.user)
    todosCompleted = todosCompleted.order_by('date')
    todosCompleted = list(filter(lambda x: x.iscompleted, todosCompleted))
    todos += todosCompleted


    global context
    context['todos'] = todos
    context['form'] = form
    context['date'] = datetime.datetime.now()
    return render(req,"mytodos.html",context)

@login_required(login_url="/users/login/")
def completeTodo(req):
    from .todoLang import lang2

    id = req.POST.get('id')
    todo = Todo.objects.filter(id = id,author = req.user)
    if(todo):
        if(todo[0].iscompleted): 
            todo[0].iscompleted = False
            todo[0].isEmailSent = False
        else: 
            todo[0].iscompleted = True
            todo[0].isEmailSent = True
        todo[0].save()
        messages.success(req,lang2['todoCompleted'])
    return HttpResponseRedirect('/todos/mytodos/')

@login_required(login_url="/users/login/")
def deleteTodo(req,id):
    from .todoLang import lang2

    todo = Todo.objects.filter(id = id,author = req.user)
    todo.delete()
    messages.success(req,lang2['todoDeleted'])
    return HttpResponseRedirect('/todos/mytodos/')

