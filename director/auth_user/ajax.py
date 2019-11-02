# encoding:utf-8

from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.contrib import auth 
from helpers.director.db_tools import get_or_none,from_dict
from helpers.director.forms import AuthForm,LoginForm
from ..model_admin.permit import has_permit
from helpers.director.kv import get_value,set_value,KVModel
import json
from django.utils import timezone

def get_globe():
    return globals()


def logout(request):
    auth.logout(request)
    return {'status':'success'}


def do_login(username,password,request,auto_login=False):
    """
    登录函数：
    """
    key = 'login_count_%s'%username
    value = get_value(key,0)
    now = (timezone.now() + timezone.timedelta(hours = 8 )).replace(tzinfo = None)
    if value:
        dc = json.loads(value)
        if timezone.datetime.strptime( dc.get('createtime') ,'%Y-%m-%d %H:%M:%S') + timezone.timedelta(hours=2) > now \
        and dc.get('count') > 5:
            return {'errors':{"password":['近期尝试登陆次数过多，请稍后再试！']}}
    form=LoginForm({'username':username,'password':password})
    
    if form.is_valid():
        user= auth.authenticate(username=username,password=password)
        if not auto_login:
            request.session.set_expiry(0)
        auth.login(request, user)
        if value:
            KVModel.objects.filter(key=key).delete()
        return {'status':'success'}
    else:
        if value:
            dc ={
                'count':dc['count']+1,
                'createtime':now.strftime('%Y-%m-%d %H:%M:%S'),
            }
        else:
            dc ={
                'createtime':now.strftime('%Y-%m-%d %H:%M:%S'),
                'count':1
            }
        set_value(key,json.dumps(dc))
        return {'errors':form.errors}

def do_login_old(username,password,request):
    """
    原来的登录函数
    """
    form=LoginForm({'username':username,'password':password})
    if form.is_valid():
        user= auth.authenticate(username=username,password=password)
        auth.login(request, user)
        return {'status':'success'}
    else:
        return {'errors':form.errors}
    #if user: 
        #if user.is_active:  
            #auth.login(request, user)
            #return {'status':'success'}
        #else:
            #raise UserWarning,'[do_login] user has been disabled'
    #else:
        #user=get_or_none(User,username=name)
        #if user:
            #raise UserWarning,'[do_login] user exist,but password not match'
        #else:
            #raise UserWarning,'[do_login] user not exist'
    #raise UserWarning,'[do_login] user or password not match'  

def registe(info):
    form = AuthForm(info)
    if form.is_valid(): 
        user=from_dict(form.cleaned_data,User)
        user.set_password(user.password)
        #user=User.objects.create_user(username=username,password=password)
        user.is_active=True
        user.save()
        return {'status':'success'}  
    else:
        return {'errors':form.errors}
    #try:
        #User.objects.get(username=username)
        #raise UserWarning,'[registe] username has exist'
    #except User.DoesNotExist:
        #user=User.objects.create_user(username=username,password=password)
        #user.is_active=True
        #user.save()
        #return {'status':'success'}
        #form=StudioForm(studio)
        #if form.is_valid():
            #studio.update(form.cleaned_data )
            #studio_obj=from_dict(studio)
            #studio_obj.save()
            #freeze_studio_with_celery(studio_obj)
            #return {'status':'success'}
        #else:
            #return {'errors':form.errors}

def changepswd(user,row):
    if row.get('first_pswd')!=row.get('second_pswd'):
        return  {'errors':{'second_pswd':['second password not match']}}
    elif not row.get('first_pswd'):
        return {'errors':{'first_pswd':['must input password']}}
        
    md_user= User.objects.get(pk=row.get('uid'))
    if user.is_superuser or has_permit(user,"myauth.modify_other_pswd")  or md_user.check_password(row.get('old_pswd')):
        md_user.set_password(row.get('first_pswd'))
        md_user.save()
        dc={'status':'success'}
    else:
        dc={'errors':{'old_pswd':['old password not match']}}

    return dc
    

