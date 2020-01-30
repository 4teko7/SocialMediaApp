# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Article(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey("auth.User",on_delete = models.CASCADE,verbose_name = "Yazar")
    title = models.CharField(max_length = 100,verbose_name = "Baslik")
    content = models.TextField(verbose_name = "Icerik")
    createdDate = models.DateTimeField(auto_now_add = True,verbose_name = "Cretated Name")

    def __str__(self):
        return "Title: {} - Author: {} - Created Date: {}".format(self.title,self.author,self.createdDate)