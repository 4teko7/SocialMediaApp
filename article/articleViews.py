# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,HttpResponse,redirect
from django.contrib import messages
from .articleForms import *

# Create your views here.
def index(req):
    # return HttpResponse("<h3>Anasayfa</h3>")
    return render(req,"index.html",{"a":"Bilal"})

def detail(req,id):
    # return HttpResponse("<h3>Anasayfa</h3>")
    context = {
        "id":id
    }
    return render(req,"index.html",context)



# Create your views here.


def addArticle(req):

    form = addArticleForm()
    context = {
            "form" : form
             }
    if(req.method == "POST"):
        form = addArticleForm(req.POST)
        if(form.is_valid()):
            article = form.save(commit = False)
            article.author = req.user
            print("ARTICLE : " , article)
            article.save()
            messages.success(req,"Article Successfully Added.")
            return redirect("mainPage")
        else:
            print("FORM IS NOT VALID")

            return render(req,"addArticle.html",context)
    else:
        return render(req,"addArticle.html",context)

