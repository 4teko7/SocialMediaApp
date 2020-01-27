from django.conf.urls import url
from django.contrib import admin
from users.userViews import *
app_name = "userroutes"
urlpatterns = [
    url("about/",about,name = "about"),
    url("register/",registerUser,name = "registerUser"),
    url("login/",loginUser,name = "loginUser"),
    url("logout/",logoutUser,name = "logoutUser"),
]