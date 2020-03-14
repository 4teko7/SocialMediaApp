# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Todo(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey("auth.User",on_delete = models.CASCADE,verbose_name = "Author")
    content = models.TextField(verbose_name = "Content")
    date = models.DateTimeField(verbose_name = "Time",default='')
    iscompleted = models.BooleanField(verbose_name = "Is Completed",default=False)
    isEmailSent = models.BooleanField(verbose_name = "Is Email Sent",default=False)
    def __str__(self):
        return "Author: {} - Created Date: {}".format(self.author,self.date)