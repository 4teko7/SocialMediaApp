#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""djangoBlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from __future__ import unicode_literals
from django.conf.urls import url,include
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib import admin
from article.models import Article
from todo.models import Todo
from todo.todoLang import todoLanguage
from article.articleLang import articleLanguage
from users.userLang import userLanguage
from comment.commentLang import commentLanguage
from .language import *
import datetime
from users.models import UserProfile
import time
from django.conf import settings
from django.conf.urls.static import static

from apscheduler.schedulers.background import BackgroundScheduler
import smtplib
import ssl
from django.template import loader
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

context = {}
allArticles = 0
myTodos = 0
myArticles = 0
lang = en
isJobStarted = False


def check(req):

    global context
    global allArticles
    if(req.user.is_authenticated):
        allInfo(req)
        context = {
            "allArticles":allArticles,
            "myTodos":myTodos,
            "myArticles":myArticles
             }
    else:
        allArticles = len(Article.objects.filter(isPrivate = False))
        context = {"allArticles":allArticles}


def allInfo(req):
    global allArticles
    global myTodos
    global myArticles
    allArticles = len(Article.objects.filter(isPrivate = False))
    myTodos = len(Todo.objects.filter(author = req.user))
    myArticles = len(Article.objects.filter(author = req.user))



def mainPage(req):
    start_job()
    global lang
    global context

    check(req)
    if(req.user.is_authenticated):

        articles = Article.objects.filter(author = req.user)
        articles = articles.order_by('id')
        articles = articles[::-1]
        articles = list(articles[:4])
        context['articles'] = articles


        todos = Todo.objects.filter(author = req.user)
        todos = todos.order_by('date')
        todos = list(filter(lambda x: not x.iscompleted, todos))
        todos = todos[:4]
        context['todos'] = todos

        profile = UserProfile.objects.filter(user = req.user)
        if(profile):
            if(profile[0].profileImage):
                context['profileImage'] = profile[0].profileImage
    context['date'] = datetime.datetime.now()
    context['lang'] = lang
    return render(req,"index.html",context)



def searchArticle(req):
    global context
    global lang
    check(req)
    context['lang'] = lang
    keywords = req.GET.get('keywords')
    if(keywords):
        articles = Article.objects.filter(title__contains = keywords)
        context['articles'] = articles
    return render(req,'allarticles.html',context)

def searchUser(req):
    global context
    global lang
    check(req)
    keywords = req.GET.get('keywords')
    context['lang'] = lang
    if(keywords):
        users = User.objects.filter(username__contains = keywords)

        context['users'] = users
    return render(req,'allusers.html',context)



def language(req):
    global lang
    global context
    if(lang['language'] == "ENGLISH"): lang = en
    else: lang = tr
    context['lang'] = lang

    todoLanguage(lang)
    articleLanguage(lang)
    userLanguage(lang)
    commentLanguage(lang)
    return redirect(req.GET.get("currentPage"))


urlpatterns = [
    url(r'admin/', admin.site.urls),
    url('users/', include("users.userRoutes")),
    url("articles/",include("article.articleRoutes")),
    url("todos/",include("todo.todoRoutes")),
    url('searchArticle/',searchArticle,name = 'searchArticle'),
    url('searchUser/',searchUser,name = "searchUser"),
    url('comments/',include('comment.commentRoutes')),
    url('language/',language,name = "language"),
    url('^$',mainPage,name = "mainPage"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)





scheduler = BackgroundScheduler()
job = None

def tick():
    print("IT CHECKS @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    todos = Todo.objects.all()
    todos = todos.order_by('date')
    todos = list(filter(lambda x: not x.iscompleted, todos))
    for todo in todos:

        year = str(time.localtime(time.time()).tm_year)
        mon = str(time.localtime(time.time()).tm_mon)
        day = time.localtime(time.time()).tm_mday

        if(len(mon) < 2):
            mon = '0' + mon

        todoYear = str(todo.date)[0:4]
        todoMon = str(todo.date)[5:7]
        todoDay = str(todo.date)[8:11]
        # print("{} : {} : {}".format(todoYear,todoMon,int(todoDay)+1))
        # print("{} : {} : {}".format(year,mon,day))
        # print()
        if(todoYear == year and todoMon == mon):
            if(todoDay == "31"):
                if(day == 1):
                    #Send Email
                    if(not todo.isEmailSent):
                        sendEmail(todo)
            elif(int(todoDay)+1 == day):
                    #SEND EMAIL
                # print(not todo.isEmailSent)
                if(not todo.isEmailSent):
                    # print("BURAYA GELDI")
                    sendEmail(todo)


        # print("Time to : ",todo.content)


def start_job():
    global isJobStarted
    if(not isJobStarted):
        print("IT WILL START JOB")
        global job
        job = scheduler.add_job(tick,'interval', seconds=120)
        try:
            isJobStarted = True
            scheduler.start()
        except:
            pass


def sendEmail(todo):
	
    port = settings.EMAIL_PORT
    smtp_server = settings.EMAIL_HOST
    sender_email = settings.EMAIL_HOST_USER
    password = settings.EMAIL_HOST_PASSWORD
    receiver_email = todo.author.email
    subject = "Bugun Yapman Gerekenler !"


    # body = todo.content
    # message2 = 'Subject: {}\n\n{}'.format(subject, body)
    context = ssl.create_default_context()
    email_content = loader.render_to_string(
            'message.html',
            {
                'Content-Type': 'text/html; charset=utf-8',
                'Content-Disposition': 'inline',
                'Content-Transfer-Encoding': '8bit',
                'date': datetime.datetime.now().strftime('%a, %d %b %Y  %H:%M:%S %Z'),
                'X-Mailer': 'python',
                'subject': subject,
                'todo':  todo.content,
                    }
        )
    

    MESSAGE = MIMEMultipart('alternative')
    MESSAGE['subject'] = subject
    MESSAGE['To'] = receiver_email
    MESSAGE['From'] = sender_email
    MESSAGE.preamble = """
Your mail reader does not support the report format.
Please visit us <a href="https://socialtodos.herokuapp.com/">online</a>!"""
 
    HTML_BODY = MIMEText(email_content, 'html')
 
    MESSAGE.attach(HTML_BODY)




    # print("IT IS HERE !")
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        # print("IT IS HERE ! @@@@@@@@@@@")
        server.login(sender_email, password)
        # print("INN SEND EMAIL METHOD BEFORE MESSAGING")
        try:
        	# html_message=message,
            server.sendmail(sender_email, receiver_email, MESSAGE.as_string())
            print("EMAIL GONDERILDI")
            todo.isEmailSent = True
            # print("EMAIL ATTI @@@@@@@@@@@@@@@@@@@@@@@")
            todo.save()

        except:
            print("EMAIL ATARKEN HATA ALDI")
        finally:
            print("QUIT FROM SERVER *****************************************************")
            server.quit()
           
