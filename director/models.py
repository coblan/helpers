# encoding:utf-8
from __future__ import unicode_literals

from django.contrib.auth.models import User,Group
from django.db import models
from django.utils.translation import ugettext as _
from .model_func.jsonfield import JsonField

class LogModel(models.Model):
    "操作日志"
    operation = models.CharField('操作类型',max_length=100,blank=True)
    tag = models.CharField('标签',max_length=100,blank=True,help_text='用户快速查询')
    detail =models.TextField('详细',blank=True)
    creattime = models.DateTimeField('产生时间',auto_now=True)
    user= models.ForeignKey(User,verbose_name="操作人",blank=True,null=True)

# class PermitGroup(models.Model):
    # name = models.CharField('权限组名称',max_length=300)
    # permit=models.ManyToManyField('PermitModel',verbose_name="权限")
    # desp=models.TextField(verbose_name="描述",blank=True)

class PermitModel(models.Model):
    group = models.OneToOneField(Group)
    names = models.TextField(default= '')

#class PermitModel(models.Model):
    #name = models.CharField('权限名称',max_length=300)
    #group = models.ManyToManyField(Group,verbose_name=_('user group'),blank=True,null=True)
    ## group = models.OneToOneField(Group,verbose_name=_('user group'))
    ## model = models.CharField('model',max_length=200, default='')
    #permit = JsonField(verbose_name=_('user permit'),default={})
    #desp=models.TextField(verbose_name="描述",blank=True)
    
    #def __str__(self):
        #return self.name




# Create your models here.
EDITOR_TYPE=(
    ('blocktext','普通编辑器'),
    ('richtext','富文本编辑器'),
)

class KVModel(models.Model):
    key=models.CharField('key',max_length=100,blank=True,unique=True)
    value=models.TextField(verbose_name='value',blank=True)
    update = models.DateTimeField(auto_now=True)
    #update=models.DateTimeField(auto_now=True)
    #editor_type=models.CharField('编辑器类型',max_length=30,default='blocktext',choices=EDITOR_TYPE)