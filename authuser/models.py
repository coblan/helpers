from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

GEN_CHOICE = (
    #(0, '未知'), 
    (1, '男'), 
    (2, '女'), 
)

# Create your models here.
class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField('手机号', max_length = 30, blank = True)
    addr = models.CharField('地址', max_length = 300, blank = True)
    id_code = models.CharField('身份证号码', max_length = 30, blank = True)
    gender = models.IntegerField('性别', default= 1, choices= GEN_CHOICE, blank = True)
    nickname =  models.CharField('昵称', max_length = 200, blank = True)
    head = models.CharField('头像', max_length = 300, blank = True)
    birthday = models.DateField(verbose_name= '出生日期', blank = True, null = True)
    address = models.CharField(verbose_name = '地址', max_length = 500, blank = True)
    
    class Meta:
        abstract = True    

class ValidatorCode(models.Model):
    code = models.CharField('验证码', max_length = 30)
    valid = models.BooleanField('是否有效', default = True)
    create_time = models.DateTimeField(auto_now_add= True)

class PhoneCode(models.Model):
    phone = models.CharField('手机号', max_length = 30, blank = True)
    code = models.CharField('验证码', max_length = 30)
    valid = models.BooleanField('是否有效', default = True)
    create_time = models.DateTimeField(auto_now_add= True)

class LoggedInUser(models.Model):
    user = models.OneToOneField(User, related_name='logged_in_user')
    # Session keys are 32 characters long
    session_key = models.CharField(max_length=32, null=True, blank=True)

    def __str__(self):
        return self.user.username

class PasswordInfo(models.Model):
    user = models.OneToOneField(User,)
    #need_change = models.BooleanField(verbose_name='是否需要修改',default=True)
    last_change = models.DateTimeField(verbose_name='上次修改时间',blank=True,null=True)
    memo = models.TextField('备注',blank=True)
    
    
    
    
