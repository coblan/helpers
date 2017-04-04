# encoding:utf-8

from __future__ import unicode_literals
from __future__ import absolute_import
from django.shortcuts import render
from django.core.urlresolvers import reverse
from . import ajax
from .container import evalue_container
from .model_admin.permit import Permit
from .port import jsonpost

class BaseEngine(object):
    _pages={}
    menu={}
    
    def add_pages(self,dc):
        self._pages.update(dc)
    
    def view(self,request,name):
        page_cls = self._pages.get(name)
        if request.method=='GET':
            page=page_cls(request)
            ctx=page.get_context()
            ctx['menu']=self.get_menu(request)
            return render(request,page.template,context=ctx)
        elif request.is_ajax():
            return jsonpost(request,ajax.get_globle())        
        
    def get_menu(self,request):
        return evalue_container( self.menu,user=request.user )

def can_touch(model):
    def _func(user):
        validator = Permit(model, user)
        return validator.can_access()
    return _func

def can_list(ls):
    def _func(user):
        for model in ls:
            validator = Permit(model, user)
            if validator.can_access():
                return True
    return _func    

def page(name):
    return lambda: reverse('model_table',kwargs={'name':name})

def fa(name):
    return '<i class="fa %s" aria-hidden="true"></i>'%name


