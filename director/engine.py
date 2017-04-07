# encoding:utf-8

from __future__ import unicode_literals
from __future__ import absolute_import
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.conf import settings
from .model_admin import ajax
from .container import evalue_container
from .model_admin.permit import ModelPermit
from .port import jsonpost
from .pages import DelPage

page_dc={}

class BaseEngine(object):
    _pages=None
    menu={}
    url_name='baseengine'
    
    @classmethod
    def as_view(cls):
        if not getattr(cls,'_single',None):
            cls._single = cls()
        return cls._single.view
    
    @classmethod
    def add_pages(cls,dc):
        if cls._pages is None:
            cls._pages={
                'del_rows':DelPage,
            }
        cls._pages.update(dc)
    
    def view(self,request,name):
        page_cls = self._pages.get(name)
        if request.method=='GET':
            if getattr(page_cls,'need_login',True):
                if request.user.is_anonymous() or not request.user.is_active:
                    return redirect(settings.LOGIN_URL+'?next='+request.get_full_path())
                
            page=page_cls(request)
            ctx=page.get_context()
            ctx['menu']=self.get_menu(request)
            ctx['page_name']=name
            ctx['engine_url']=reverse(self.url_name,args=('aa',))[:-3]
            return render(request,page.template,context=ctx)
        elif request.is_ajax():
            return jsonpost(request,ajax.get_globle())        
        
    def get_menu(self,request):
        return evalue_container( self.menu,user=request.user,url_name=self.url_name)

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

def page(name):
    return lambda url_name: reverse(url_name,args=(name,))

def fa(name):
    return '<i class="fa %s" aria-hidden="true"></i>'%name

