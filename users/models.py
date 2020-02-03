
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from ckeditor.fields import RichTextField
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
# Create your models here.

class UserProfile(models.Model):
    from .userLang import lang2
    user = models.OneToOneField(User)
    username2 = models.CharField(max_length = 30,verbose_name = lang2['username'])
    # email = models.EmailField(max_length = 70,verbose_name = lang2['email'])
    # name = models.CharField(max_length = 30,verbose_name = lang2['firstname'])
    # surname = models.CharField(max_length = 30,verbose_name = lang2['lastname'])

    profileImage = models.ImageField(upload_to = 'profileimg',blank = True,null = True,verbose_name = "Resim Ekle/Add Picture")
    def __str__(self):
        return self.user.username

def create_profile(sender,**kwargs):
    if(kwargs['created']):
        userProfile = UserProfile.objects.create(user=kwargs['instance'])
post_save.connect(create_profile,sender = User)