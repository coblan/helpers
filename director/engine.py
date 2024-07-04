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
from django.http import HttpResponse,JsonResponse,Http404
#from .model_admin import ajax
from helpers.func.collection.container import evalue_container,find_one_r
from .access.permit import ModelPermit,has_permit
#from helpers.func.network.ajax_router import jsonpost

from django.db import models
from django.core.exceptions import PermissionDenied
import inspect
import json
from django.views.decorators.cache import patch_cache_control
import time
from django.shortcuts import redirect
from .base_data import js_tr_list,js_lib_list
from django.views.decorators.csrf import csrf_exempt
from helpers.director.middleware.request_cache import get_request_cache
from urllib.parse import unquote
from django.utils.translation import gettext as _

import logging
general_log = logging.getLogger('general_log')
gb={}


class BaseEngine(object):
    _pages=None
    menu={}
    url_name='baseengine'
    brand = 'Admin System'
    mini_brand = 'AdSys'
    title = 'Admin'
    prefer='pc'
    login_url= '/pc/login' # getattr( settings,'LOGIN_URL','/pc/login')
    logout_url = '/pc/logout?next=/'
    #login_url=getattr( settings,'LOGIN_URL','/accounts/login')
    #logout_url = '/accounts/logout'
    need_login = True
    menu_search = True
    ui_theme='skin-blue'
    home = '/' # 当前engine的主页，没有目的的时候，可以往这里跳
    
    root_page='/'   # 被home 替代了
    access_from_internet = True # getattr(settings,'ACCESS_FROM_INTERNET',False)
    need_staff = False
    forbid_pages =[]
    
    
    @classmethod
    def as_view(cls):
        if cls.__name__ not in gb:
            gb[cls.__name__] = cls()
        return gb[cls.__name__].view
        #if not getattr(cls,'_singleton',None):
            #cls._singleton = cls()
        #return cls._singleton.view
    
    @classmethod
    def add_pages(cls,dc):
        if cls._pages is None:
            cls._pages=[]
        if not dc in cls._pages:
            cls._pages.append(dc)
    
    def login_authorized(self,request):
        if request.user.is_superuser:
            return True
        if request.user.is_anonymous(): 
            return False
        elif not request.user.is_active:
            raise PermissionDenied('Your account have been Deactive!')
        #elif not request.user.is_active or not request.user.is_staff:
            #raise PermissionDenied('No permit! You should be Active User OR staff to access this System,')
        else:
            return True
    @csrf_exempt 
    def view(self,request,name):    
        if name in self.forbid_pages:
            raise PermissionDenied('页面禁止访问')
        self.request = request
        self.engin_url =  reverse(self.url_name,args=('aa',))[:-3]
        
        page_cls = self.get_page_cls(name)
        # 如果需要从定向director页面
        if hasattr(page_cls,'directorPage'):
            page_cls = page_cls.directorPage(request,name) or page_cls
        #if not page_cls:
            #raise Http404()
        
        if hasattr(page_cls, 'need_login'):
            need_login = page_cls.need_login
        else:
            need_login = self.need_login
        if need_login and not self.login_authorized(request):
            return redirect(self.login_url+'?next='+ unquote( request.get_full_path()) )
        
        # 用在403页面内
        request.engin={
            'login_url':self.login_url+'?next='+ unquote( request.get_full_path())
        }
        
        
        if need_login and  not request.user.is_staff:
            if hasattr(page_cls, 'need_staff'):
                if getattr(page_cls, 'need_staff'):
                    raise PermissionDenied('只有职员才能登陆后台界面!')
            elif self.need_staff:
                raise PermissionDenied('只有职员才能登陆后台界面!')
        
        try:
            page=page_cls(request, engin = self)
            if hasattr(page, 'check_permit'):
                check_rt = page.check_permit()
                # 可以在这里检测权限，然后跳转
                if isinstance(check_rt, HttpResponse):
                    return check_rt
            ctx=page.get_context()
        except UserWarning as e:
            if  request.is_ajax():
                return JsonResponse({'success':False,'msg':str(e)})
            else:
                return HttpResponse(str(e))
        # 如果返回的事 HttpResponse，表示已经处理完毕了，不需要附加其他属性。
        if isinstance(ctx, HttpResponse):
            return ctx
        
        # 如果是ajax请求，则只返回业务数据
        if  request.is_ajax() and not request.GET.get('_ajax_html') : #and not getattr(page,'ajax_html',False):
            resp= HttpResponse(json.dumps(ctx),content_type="application/json")
        if request.GET.get('_accept')=='json' or 'json' in request.META.get('HTTP_ACCEPT',''):
            resp= HttpResponse(json.dumps(ctx,ensure_ascii=False),content_type="application/json") 
        else:
            named_ctx = get_request_cache()['named_ctx']
            if ctx.get('named_ctx'):
                named_ctx.update(ctx.get('named_ctx'))
            ctx['named_ctx'] = evalue_container( named_ctx)
            ctx['engine_name'] = self.url_name
            ctx['brand'] = self.brand
            ctx['title'] = self.title
            ctx['menu_search']=self.menu_search
            ctx['menu']=self.get_menu(request)   
            ctx['page_name']=name
            ctx['engin_url']= self.engin_url
            if isinstance(self.root_page,(str,str)):
                ctx['root_page']=self.root_page
            else:
                ctx['root_page']=self.root_page(self.url_name)
            
            if hasattr(page,'get_template'):
                template=page.get_template()
            else:
                template=page.template
            #ctx=self.get_ctx(ctx)
            ctx['template']= template
            ctx['ui_theme'] = self.ui_theme
            if self.request.GET.get('_embed'):
                ctx['body_class']= 'embed'
            if hasattr(page,'get_label'):
                ctx['page_label'] =page.get_label()
            ctx['head_bar_data']=self.get_head_bar_data(request)
            ctx['js_config'] = self.getJsConfig()
            if hasattr(page,'getExtraJs'):
                ctx['extra_js'] = page.getExtraJs(ctx)
            ctx=self.custome_ctx(ctx)
            resp= render(request,template,context=ctx)
        if getattr(page,'get_cache_control',None):
            kw= page.get_cache_control()
            patch_cache_control(resp,**kw)
        if getattr(page,'processRespons',None):
            page.processRespons(resp)
        return resp
       
    def custome_ctx(self,ctx):
        return ctx
    
    def get_url(self,name):
        return reverse(self.url_name,args=(name,))
    
    def get_head_bar_data(self,request):
        user = request.user
        if user.is_anonymous:
            username = 'anonymous'
        else:
            username = user.first_name or  user.username
        return {
            'user':{
                'first_name':user.first_name if user.is_authenticated else 'AnonymousUser',
                    'username':user.username,
                    },
            'brand':self.brand,
            'mini_brand':self.mini_brand ,
            'header_bar_widgets': [
                #{'editor': 'com-headbar-user-info', 'first_name': username, 'username': username,'logout_url':self.logout_url },
                
                {"name":'userinfo', "editor":'com-head-dropmenu','label':username,'options':[
                        {'click_express':f'location="/accounts/pswd"','label':_('修改密码') },
                        {'click_express':f'location="{self.logout_url}"','label':_('退出') },
                                    ]},
                ],
        }
    def get_page_cls(self,name):
        if self._pages:
            for dc in self._pages:
                if name in dc:
                    return dc[name]

    def get_menu(self,request):
        menu = evalue_container( self.menu,request=request,user=request.user,url_name=self.url_name)
        ls = []
        for act in menu:
            if 'submenu' in act:
                for act2 in list( act['submenu']):
                    if 'submenu' in act2:
                        if not act2['submenu']:
                            act['submenu'].remove(act2)                
                if not act['submenu']:
                    continue
               
            ls.append(act)
        return ls
    
    def getJsConfig(self):
        lans = []
        for k,v in settings.LANGUAGES:
            lans.append({'value':k,'label':v})
        def_lan = settings.LANGUAGE_CODE
        crt_lan =  getattr(self.request,'LANGUAGE_CODE',def_lan) #self.request.LANGUAGE_CODE #self.request.COOKIES.get('django_language', def_lan)
        
        tr_dc = {}
        for fun in js_tr_list:
            tr_dc.update(fun())
        
        lib_dc = {}
        self.request.META['ACCESS_FROM_INTERNET'] = self.access_from_internet
        self.request.META['ENGIN'] = self
        for fun in js_lib_list:
            lib_dc.update(fun(self.request))
        return {
            'lans':lans,
            'crt_lan': crt_lan,
            'tr':tr_dc ,
            'js_lib':lib_dc,
            'is_debug':settings.DEBUG,
            'login_url':self.login_url,
            'static_url':settings.STATIC_URL,
        }
    

def and_list(ls):
    def _func(user):
        for model in ls:
            if isinstance(model,models.Model) or(inspect.isclass(model) and issubclass(model,models.Model)):
                validator = ModelPermit(model, user)
                if not validator.can_access():
                    return False
            elif isinstance(model,(str,str)):
                if not has_permit(user,model): # model是字符串，表示是验证特殊权限
                    return False
            elif inspect.isfunction(model):
                if not model(user):
                    return False
        return True
    return _func   

def can_touch(model, user):
    #def _func(user):
    validator = ModelPermit(model, user)
    return validator.can_access()
    #return _func

def can_list(ls):
    def _func(user):
        for model in ls:
            validator = ModelPermit(model, user)
            if validator.can_access():
                return True
    return _func    

def page(name,append=''):   
    def _func(url_name,user):
        if callable(append):
            append_str=append(user) 
        else:
            append_str=append
        return reverse(url_name,args=(name,))+append_str
    return _func
    # return lambda url_name: reverse(url_name,args=(name,))+append


def fa(name):
    return '<i class="fa %s" aria-hidden="true"></i>'%name




