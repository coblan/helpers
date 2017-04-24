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
from .port import jsonpost
from pydoc import locate
from django.utils.translation import ugettext as _
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
    auth.logout(request)
    return redirect(next) 

@ensure_csrf_cookie
def change_pswd(request):
    if request.method=='GET':
        dc={
            'login_url':reverse('login')
        }        
        return render(request,'authuser/changepswd.html',context=dc)
    elif request.method=='POST':
        #try:
        return jsonpost(request,auth_ajax.get_globe())  
        #except UserWarning as e:
            #return HttpResponse(json.dumps({'status':'fail','msg':str(e)}),content_type="application/json")
            

def trival(request):
    pass

def ajax_views(request,app):
    ajax=locate('%(app)s.ajax'%{'app':app})
    # if request.method=='POST':
    try:
        return jsonpost(request, ajax.get_globe())
    except KeyError as e:
        rt={'status':'error','msg':'key error '+str(e) +' \n may function name error'}
        return HttpResponse(json.dumps(rt),content_type="application/json")  