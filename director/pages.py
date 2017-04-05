
from __future__ import absolute_import
import urllib
import json
from django.apps import apps
from .model_admin.base import model_dc
import re

class TablePage(object):
    template='director/table.html'
    tableCls=''
    ajax_scope={}
    def __init__(self,request):
        self.request=request
        self.table = self.tableCls.parse_request(request)
        self.crt_user=request.user
       
    def get_context(self):
        ctx = self.table.get_context()
        #pop = self.request.GET.get('_pop')
        #if not pop:
            #menu_list=list( render_dc.get('menu') )
            #ctx['menu']=evalue_container(menu_list,user=self.request.user)        

        return ctx
    
class FormPage(object):
    template='director/fields.html'
    fieldsCls=''
    ajax_scope={}
    def __init__(self,request):
        self.request=request
        self.pk=request.GET.get('pk')
        self.fields = self.fieldsCls(pk=self.pk,crt_user=request.user)
        
    def get_context(self):
        ctx = self.fields.get_context()
        #pop = self.request.GET.get('_pop')
        #if not pop:
            #ctx['menu']=evalue_container(render_dc.get('menu'),user=self.request.user)  
        return ctx

class DelPage(object):
    template='director/del_rows.html'
    ajax_scope={}
    def __init__(self,request):
        self.request=request
    
    def get_context(self):
        ctx = {}
        # pop = self.request.GET.get('_pop')
        # if not pop:
            # ctx['menu']=evalue_container(render_dc.get('menu',{}),user=self.request.user) 
            
        ls_str = self.request.GET.get('rows')
        rows = [x for x in ls_str.split(',') if x]

        
        infos = {}
        for row in rows:
            ls = row.split(':')
            _class=ls[0]
            model = apps.get_model(_class)
            model_util= model_dc.get(model)
            fields_cls = model_util.get('fields') 
            for pk in ls[1:]:
                dc={'pk':pk,'crt_user':self.request.user}
                fields_obj= fields_cls(**dc)
                infos.update(fields_obj.get_del_info())
            
        ctx['infos']=infos
        ctx['rows']=rows       
        return ctx   