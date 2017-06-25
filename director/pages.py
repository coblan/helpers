# encoding:utf-8

from __future__ import absolute_import
import urllib
import json
from django.apps import apps
from .model_admin.base import model_dc
import re
from .model_admin.permit import ModelPermit
from .db_tools import to_dict,sim_dict,model_to_head
from .models import LogModel
from ..ex import findone
from .container import evalue_container

class TablePage(object):
    template=''
    tableCls=''
    ajax_scope={}
    def __init__(self,request):
        self.request=request
        self.table = self.tableCls.parse_request(request)
        self.crt_user=request.user
        self.permit=self.table.permit #ModelPermit(self.table.model,self.crt_user)
    
    def get_template(self,prefer=None):
        if self.template:
            return self.template
        elif prefer=='wx':
            return 'wx/table.html'
        else:
            return 'director/table.html'
        
    def get_context(self):
        ctx = self.table.get_context()
        ctx['can_add']=self.permit.can_add()
        ctx['can_del']=self.permit.can_del()
        if self.permit.changeable_fields:
            ctx['can_edit']=True
        ctx['app']=self.tableCls.model._meta.app_label
        ctx['page_label'] =self.get_label()
        return ctx
    
    def get_label(self):
        return '列表项'
    
class FormPage(object):
    template=''
    fieldsCls=''
    ajax_scope={}
    def __init__(self,request):
        self.request=request
        #self.pk=request.GET.get('pk')
        self.fields = self.fieldsCls.parse_request(request) # (pk=self.pk,crt_user=request.user,request=request)
        self.ctx=self.fields.get_context()
        
    
    def get_template(self,prefer=None): 
        if self.template:
            return self.template
        elif prefer=='wx':
            return 'wx/fields.html'
        else:
            return 'director/fields.html'
    
    def get_context(self):
        self.permit=self.fields.permit
        self.ctx['can_add']=self.permit.can_add()
        self.ctx['can_del']=self.permit.can_del()   
        self.ctx['can_log']=self.permit.can_log()
        if self.permit.changeable_fields():
            self.ctx['can_edit']=True
        else:
            self.ctx['can_edit']=False
        
        self.ctx['app']=self.fieldsCls._meta.model._meta.app_label
        self.ctx['page_label'] =self.get_label()
        return self.ctx
    
    def get_label(self):
        return '编辑表单'    

class DelPage(object):
    template=''
    ajax_scope={}
    def __init__(self,request):
        self.request=request
    
    def get_template(self,prefer=None):
        if self.template:
            return self.template
        elif prefer=='wx':
            return 'wx/del_rows.html'
        else:
            return 'director/del_rows.html'
        
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
        ctx['page_label']=self.get_label()
        return ctx   
    def get_label(self):
        return '数据表行删除'

class LogPage(object):
    template='director/model_log.html'
    def __init__(self, request):
        """
        ?rows=pkg.model:1:2,pkg.model2:1:2,
        
        """
        self.request=request
       
    
    def get_context(self):
        ls_str = self.request.GET.get('rows')
        rows_stream = [x for x in ls_str.split(',') if x]
        rows =[]
        for row in rows_stream:
            ls   = row.split(':')
            _class=ls[0]
            model = apps.get_model(_class)
            model_util= model_dc.get(model)            
            fields_cls = model_util.get('fields') 
            perm = ModelPermit(model, self.request.user)
            if perm.can_log(): 
                for pk in ls[1:]:
                    querys =LogModel.objects.filter(key='%s.%s'%(_class,pk)).order_by('-id')
                    rows.extend(list(querys))
        ctx = {'rows':[sim_dict(x,filt_attr=lambda y:{'user':unicode(y.user)}) for x in rows],
               'heads':model_to_head(LogModel)}

        ctx['can_add']=False
        ctx['can_del']=False
        return ctx         

class TabGroup(object):
    tabs=[]
    template=''
    def __init__(self, request):
        self.request=request
        tab_name=request.GET.get('_tab')
        acture_tabs=self.get_tabs()
        tab_name = tab_name or acture_tabs[0].get('name')
        self.ctx={
            'tabs':[{'name':x['name'],'label':x['label']} for x in acture_tabs],
            'crt_tab':tab_name,
        }
        tab_dict=findone(acture_tabs,{'name':tab_name}) or acture_tabs[0]
        tab_page_cls= tab_dict.get('page_cls')
        self.tab_page = tab_page_cls(request)
        self.ctx.update(self.tab_page.get_context())
    
    def get_template(self,prefer=None):
        if self.tab_page.template:
            return self.tab_page.template
        
        # 这里表示get_template方法不是继承而来的
        elif 'get_template' in self.tab_page.__class__.__dict__.keys()  and self.tab_page.get_template(prefer):
            return self.tab_page.get_template(prefer)
        elif self.template:
            return self.template
        elif prefer=='wx':
            return 'wx/tabgroup.html'
        else:
            return 'director/tabgroup.html'   
 
            
    def get_tabs(self):
        return evalue_container(self.tabs)
    
    def get_context(self):
        return self.ctx
    
    
        