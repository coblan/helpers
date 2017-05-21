#encoding:utf-8
from django.shortcuts import render,redirect
from django.http import HttpResponse
from port import jsonpost
from django.core.urlresolvers import reverse
import auth_user.ajax as auth_ajax
import json
from db_tools import form_to_head
from forms import AuthForm
from django.contrib import auth 
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.decorators import login_required
from .port import jsonpost
from pydoc import locate
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from . import ajax
import urllib

@ensure_csrf_cookie
def login(request):
    if request.method=='GET':
        next_url=request.GET.get('next','/')
        dc={
            'next':next_url,
            'regist_url':reverse('regist'),
            
        }
        return render(request,'authuser/login.html',context=dc)
  
    elif request.method=='POST':
        return jsonpost(request,auth_ajax.get_globe())
    
@ensure_csrf_cookie
def regist_user(request):
    if request.method=='GET':
        
        heads= form_to_head(AuthForm())
        for head in heads:
            if head.get('name') in ['password','pas2']:
                head['type']='password'
        dc={
            'login_url':reverse('login'),
            'heads':json.dumps( heads )
        }
        return render(request,'authuser/regist.html',context=dc)
    elif request.method=='POST':
        return jsonpost(request,auth_ajax.get_globe()) 


def logout(request):
    next = request.GET.get('next','/')
    next=urllib.unquote(next)
    auth.logout(request)
    return redirect(next) 

@ensure_csrf_cookie
@login_required
def change_pswd(request):
    pk = request.GET.get('uid')
    if pk:
        name=User.objects.get(pk=pk).username
    else:
        pk = request.user.pk
        name=request.user.username
        
    if request.method=='GET':
        dc={
            'login_url':reverse('login'),
            'username':name,
            'uid':pk
        }        
        return render(request,'authuser/changepswd.html',context=dc)
    elif request.method=='POST':
        #try:
        return jsonpost(request,auth_ajax.get_globe())  
        #except UserWarning as e:
            #return HttpResponse(json.dumps({'status':'fail','msg':str(e)}),content_type="application/json")
            

def trival(request):
    pass


"""
>5>helpers/port.rst>
总的ajax view
===============
源码路径为:director/views.ajax_views

作用是，将所有模块的ajax访问，聚集到一个url，再根据url中的app路由到不同app.ajax模块去。

该函数的url现在嵌入到了director.urls中，所以url设置为::

    from helpers.director import urls as director_urls
    url(r'^d/',include(director_urls)),
<-<
"""

def ajax_views(request,app=None):
    if not app:
        ajax_module = ajax
    else:
        ajax_module=locate('%(app)s.ajax'%{'app':app})
    try:
        return jsonpost(request, ajax_module.get_global())
    except KeyError as e:
        rt={'status':'error','msg':'key error '+str(e) +' \n may function name error'}
        return HttpResponse(json.dumps(rt),content_type="application/json")  