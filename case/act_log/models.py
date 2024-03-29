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
    
    def __str__(self):
        return '普通日志'


class BackendOperation(models.Model):
    createtime = models.DateTimeField(verbose_name='创建时间',auto_now_add=True)
    model = models.CharField('相关表', max_length=100, blank=True,)  # Field name made lowercase.
    inst_pk = models.CharField('主键',max_length=30,blank=True)
    op= models.CharField('操作',max_length=50,blank=True)
    content = models.TextField(verbose_name='内容', blank=True)  # Field name made lowercase.
    createuser = models.CharField('操作人', max_length=100, blank=True)  # Field name made lowercase.

    class Meta:
        indexes = [
            models.Index(fields=['createtime']),
        ]
    
    def __str__(self):
        return '操作日志'    

MESSAGE_LEVEL = (
    (10,'普通'),
    (20,'紧急'),
    (30,'关键')
)

class SystemMessage(models.Model):
    title = models.CharField('标题',max_length=300)
    content = models.TextField('消息内容',blank=True)
    read = models.BooleanField('是否查看',default= False)
    level = models.IntegerField('等级',choices=MESSAGE_LEVEL)
    createtime = models.DateTimeField(verbose_name='创建时间',auto_now_add=True)
    