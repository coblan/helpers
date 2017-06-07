# encoding:utf-8
from __future__ import unicode_literals

from django.contrib.auth.models import User,Group
from django.db import models
from django.utils.translation import ugettext as _


class LogModel(models.Model):
    at = models.DateTimeField(auto_now=True)
    user= models.ForeignKey(User,verbose_name=_('operator'),blank=True,null=True)
    key =models.CharField('key',max_length=200,blank=True)
    kind = models.CharField(_('kind'),max_length=100,blank=True)
    detail =models.TextField(_('detail'),blank=True)
    
    

class PermitModel(models.Model):
    group = models.OneToOneField(Group,verbose_name=_('user group'))
    # model = models.CharField('model',max_length=200, default='')
    permit = models.TextField(verbose_name=_('user permit'),default='{}')

EDITOR_TYPE=(
    ('blocktext','普通编辑器'),
    ('richtext','富文本编辑器'),
)

class KVModel(models.Model):
    key=models.CharField('key',max_length=500,blank=True)
    value=models.TextField(verbose_name='value',blank=True)
    editor_type=models.CharField('编辑器类型',max_length=30,default='blocktext',choices=EDITOR_TYPE)
