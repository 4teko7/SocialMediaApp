# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,HttpResponse

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
