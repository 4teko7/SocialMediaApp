# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from ckeditor.fields import RichTextField
from django.db import models
# Create your models here.

class Article(models.Model):
    from .articleLang import lang2
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey("auth.User",on_delete = models.CASCADE,verbose_name = lang2['author'])
    title = models.CharField(max_length = 100,verbose_name = lang2['title'])
    #content = models.TextField(verbose_name = lang2['content'])
    content = RichTextField()
    createdDate = models.DateTimeField(auto_now_add = True,verbose_name = lang2['createdDate'])
    isPrivate = models.BooleanField(verbose_name = "Gizli/Private",default=False)
    articleImage = models.ImageField(blank = True,null = True,verbose_name = "Resim Ekle/Add Picture")

    class Meta:
        ordering = ['-createdDate']

    def __str__(self):
        return "Title: {} - Author: {} - Created Date: {}".format(self.title,self.author,self.createdDate)