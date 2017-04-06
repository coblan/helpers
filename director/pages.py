
from __future__ import absolute_import
import urllib
import json
from django.apps import apps
from .model_admin.base import model_dc
import re
from .model_admin.permit import ModelPermit
from .db_tools import to_dict

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
        perm = ModelPermit(self.table.model,self.crt_user)
        ctx['can_add']=perm.can_add()
        ctx['can_del']=perm.can_del()
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
        self.ctx=self.fields.get_context()
        
    def get_context(self):
        if self.fieldsCls:
            perm = ModelPermit(self.fieldsCls.Meta.model,self.request.user)
            self.ctx['can_add']=perm.can_add()
            self.ctx['can_del']=perm.can_del()   
            self.ctx['can_log']=perm.can_log()
        return self.ctx

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
        rows_stream = [x for x in ls_str.split(',') if x]

        
        infos = {}
        rows=[]
        for row in rows_stream:
            ls = row.split(':')
            _class=ls[0]
            model = apps.get_model(_class)
            model_util= model_dc.get(model)
            fields_cls = model_util.get('fields') 
            for pk in ls[1:]:
                dc={'pk':pk,'crt_user':self.request.user}
                fields_obj= fields_cls(**dc)
                infos.update(fields_obj.get_del_info())
                rows.append(to_dict(fields_obj.instance,include=fields_obj.permit.readable_fields()))
        ctx['infos']=infos
        ctx['rows']=rows       
        return ctx   