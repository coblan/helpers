# encoding:utf-8
"""
>->helpers/engine.rst>
================
director engine
================

步骤
=====

1. 自定义engine::

    class XicheEngine(BaseEngine):
        menu=[
        {'label':'home','url':'/home','icon':fa('fa-home')},
        ...

2. 加入页面主要有两种方式，一种是baseengine.add_pages(dc),一种是base.page_dc.update(dc).
如果用的是第二种方式，需要调用add_pages(page_dc)

3. 在总的url.py文件中注册engine的入口地址::

    url(r'^d/([\w\.]+)',XicheEngine.as_view(),name=XicheEngine.url_name)

说明
=====
*. add_pages时传入的字典，记载了各个页面之间的逻辑关系。例如::

    dc={'user':usertablepage,'user.edit':userformpage}

<-<
"""
from __future__ import unicode_literals
from __future__ import absolute_import
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.conf import settings
from django.http import HttpResponse
from .model_admin import ajax
from .container import evalue_container,find_one_r
from .model_admin.permit import ModelPermit,has_permit
from .port import jsonpost
from .pages import DelPage,LogPage
from .model_admin.base import page_dc
from django.db import models
from django.core.exceptions import PermissionDenied
import inspect
import json

page_dc.update({
        'del_rows':DelPage,
        'log':LogPage,
    } )

class BaseEngine(object):
    _pages=None
    menu={}
    url_name='baseengine'
    prefer='pc'
    login_url=settings.LOGIN_URL
    root_page='/'
    #def __init__(self):
        #self.root_page='/'
        
    @classmethod
    def as_view(cls):
        if not getattr(cls,'_singleton',None):
            cls._singleton = cls()
        return cls._singleton.view
    
    @classmethod
    def add_pages(cls,dc):
        if cls._pages is None:
            cls._pages=[]
        if not dc in cls._pages:
            cls._pages.append(dc)
    
    def view(self,request,name):
        #if request.is_ajax():
              
        page_cls = self.get_page_cls(name)
        
        if getattr(page_cls,'need_login',True):
            if request.user.is_anonymous() or not request.user.is_active:
                return redirect(self.login_url+'?next='+request.get_full_path())
                
        page=page_cls(request)
        ctx=page.get_context()
        if  request.is_ajax():
            return HttpResponse(json.dumps(ctx),content_type="application/json")
        else:
            ctx['menu']=self.get_menu(request)   
            ctx['page_name']=name
            ctx['engine_url']=reverse(self.url_name,args=('aa',))[:-3]
            if isinstance(self.root_page,(str,unicode)):
                ctx['root_page']=self.root_page
            else:
                ctx['root_page']=self.root_page(self.url_name)
            
            if hasattr(page,'get_template'):
                template=page.get_template(prefer=self.prefer)
            else:
                template=page.template
            ctx=self.get_ctx(ctx)
            ctx['template']=template
            ctx=self.custome_ctx(ctx)
            return render(request,template,context=ctx)
       
            
    def custome_ctx(self,ctx):
        return ctx
    
    def get_page_cls(self,name):
        if self._pages:
            for dc in self._pages:
                if name in dc:
                    return dc[name]

    def get_menu(self,request):
        return evalue_container( self.menu,request=request,user=request.user,url_name=self.url_name)
    
    def get_ctx(self,ctx):
        """ctx的hook"""
        return ctx

def and_list(ls):
    def _func(user):
        for model in ls:
            if isinstance(model,models.Model) or(inspect.isclass(model) and issubclass(model,models.Model)):
                validator = ModelPermit(model, user)
                if not validator.can_access():
                    return False
            elif isinstance(model,(unicode,str)):
                if not has_permit(user,model): # model是字符串，表示是验证特殊权限
                    return False
            elif inspect.isfunction(model):
                if not model(user):
                    return False
        return True
    return _func   

def can_touch(model):
    def _func(user):
        validator = ModelPermit(model, user)
        return validator.can_access()
    return _func

def can_list(ls):
    def _func(user):
        for model in ls:
            validator = ModelPermit(model, user)
            if validator.can_access():
                return True
    return _func    

def page(name,append=''):
    return lambda url_name: reverse(url_name,args=(name,))+append

def fa(name):
    return '<i class="fa %s" aria-hidden="true"></i>'%name



