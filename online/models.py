#coding:utf8
from django.db import models
from django.contrib import admin


# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=150)
    password = models.CharField(max_length=100)

    def __unicode__(self):
        return self.username


class Blogs(models.Model):
    title = models.CharField(max_length=200)
    pic1 = models.ImageField('图片',upload_to='uploadImages',blank=True,null=True)
    pic1_w = models.CharField(max_length=20,blank=True,null=True)
    pic1_h = models.CharField(max_length=20,blank=True,null=True)
    item = models.CharField(max_length=50)
    pub_date = models.DateField()
    puber = models.CharField(max_length=50,blank=True,null=True)
    views = models.IntegerField(max_length=100)
    content = models.TextField(max_length=5000)

    def __unicode__(self):
	return self.title


class Comments(models.Model):
    blogid = models.CharField(max_length=20)
    blogtitle = models.CharField(max_length=300)
    pub_date = models.CharField(max_length=100)
    username = models.CharField(max_length=200,blank=True,null=True)
    ipaddress = models.CharField(max_length=50)
    content = models.TextField(max_length=1000)

    def __unicode__(self):
        return self.blogtitle

class IndexViews(models.Model):
    view_date = models.CharField(max_length=100)
    view_sum = models.CharField(max_length=100)
    view_ip = models.CharField(max_length=50)
     
    def __unicode__(self):
        return self.view_date


class PhotoViews(models.Model):
    view_date = models.CharField(max_length=100)
    view_sum = models.CharField(max_length=100)
    view_ip = models.CharField(max_length=50)
    view_user = models.CharField(max_length=50)

    def __unicode__(self):
        return self.view_date
