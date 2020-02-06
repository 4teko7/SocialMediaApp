from django.conf.urls import url
from django.contrib import admin
from todo.todoViews import *
app_name = "todoRoutes"
urlpatterns = [
    url("addtodo/",addTodo,name = "addtodo"),
    url("mytodos/",myTodos,name = "mytodos"),
    url("completetodo/",completeTodo,name = "completetodo"),
    url("deletetodo/(?P<id>\d+)/",deleteTodo,name = "deletetodo"),
    url("edittodo/(?P<id>\d+)/",editTodo,name = "editTodo"),


]