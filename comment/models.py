# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from article.models import Article

# Create your models here.

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey("auth.User",on_delete = models.CASCADE,verbose_name = "Yazar")
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    content = models.TextField(max_length = 250,verbose_name = "Add Comment")
    createdDate = models.DateTimeField(auto_now_add = True,verbose_name = "Cretated Date")

    def __str__(self):
        return "Id: {} - Author: {} - Article : {} - Created Date: {}".format(self.id,self.author,self.article,self.createdDate)