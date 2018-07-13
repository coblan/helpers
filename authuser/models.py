from __future__ import unicode_literals

from django.db import models

GEN_CHOICE = (
    (0, '未知'), 
    (1, '男'), 
    (2, '女'), 
)

# Create your models here.
class UserInfo(models.Model):
    phone = models.CharField('联系电话', max_length = 30, blank = True)
    addr = models.CharField('地址', max_length = 300, blank = True)
    id_code = models.CharField('身份证号码', max_length = 30, blank = True)
    gender = models.IntegerField('性别', default= 0, choices= GEN_CHOICE, blank = True)
    
    
