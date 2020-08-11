from django.db import models

# Create your models here.

class GeneralLog(models.Model):  
    createtime = models.DateTimeField(verbose_name='创建时间',)
    level = models.CharField('等级',max_length=20,blank=True)
    message =  models.TextField(verbose_name='消息体',blank=True)
    path = models.CharField('消息来源',max_length=300,blank=True)
    process = models.CharField('进程ID',max_length=100,blank=True)
    host = models.CharField('主机名',max_length=200,blank=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['createtime']),
        ]


class BackendOperation(models.Model):
    createtime = models.DateTimeField(verbose_name='创建时间',)
    model = models.CharField('相关表', max_length=100, blank=True,)  # Field name made lowercase.
    content = models.TextField(verbose_name='内容', blank=True)  # Field name made lowercase.
    createuser = models.CharField('操作人', max_length=100, blank=True)  # Field name made lowercase.


    class Meta:
        indexes = [
            models.Index(fields=['createtime']),
        ]