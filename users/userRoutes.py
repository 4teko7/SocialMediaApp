from django.conf.urls import url
from django.contrib import admin
from users.userViews import *
app_name = "userroutes"
urlpatterns = [
    url("about/",about,name = "about"),
    url("register/",registerUser,name = "registerUser"),
    url("login/",loginUser,name = "loginUser"),
    url("logout/",logoutUser,name = "logoutUser"),
    url("editprofile/",editProfile,name = "editprofile"),
    url("saveprofile/",saveProfile,name = "saveprofile"),
    url("changepassword/",changePassword,name = "changepassword"),
    url("changeusername/",changeUsername,name = "changeusername"),
    url("profile/(?P<id>\d+)/",profile,name = "profile"),

]