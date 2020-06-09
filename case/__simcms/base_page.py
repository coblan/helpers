from django.shortcuts import render
from helpers.director.shortcut import director
from .models import CmsPageModel
import json
from django.conf import settings
from helpers.director.base_data import js_tr_list,js_lib_list

class BasePage(object):
    
    def __init__(self, request = None,dc = {},crt_user= None , *args, **kwargs): 
        self.request = request
        self.row = dict(dc)
        
    def getName(self): 
        return '基本页面'    
    
    def is_valid(self): 
        return True
    
    def mergeCtx(self, par, ctx): 
        dc = dict(par)
        dc.update(ctx)
        return dc
    
    def get_row(self): 
        return self.pure_row
    
    def save_form(self): 
        page = CmsPageModel.objects.get(pk = self.row['_page'])
        self.pure_row = {k: v for k, v in self.row.items() if not k.startswith('_')}
        page.content = json.dumps(self.pure_row)
        page.save()
    
    def render(self, page_data): 
        template = self.getTemplate()
        ctx = {
            'js_config': self.getJsConfig(), 
            'page_data': page_data,
            }
        ctx.update(self.getContext())
        
        return render(self.request, template, context=  ctx )
    
    def getTemplate(self): 
        return ''
    
    
    def getContext(self): 
        """
        这个函数逻辑，用于显示
        """
        return {
        }
    
    def getJsConfig(self):
        lans = []
        for k,v in settings.LANGUAGES:
            lans.append({'value':k,'label':v})
        def_lan = settings.LANGUAGE_CODE
        crt_lan = self.request.COOKIES.get('django_language', def_lan)
        
        tr_dc = {}
        for fun in js_tr_list:
            tr_dc.update(fun())
        
        lib_dc = {}
        for fun in js_lib_list:
            lib_dc.update(fun(self.request))
        return {
            'lans':lans,
            'crt_lan': crt_lan,
            'tr':tr_dc ,
            'js_lib':lib_dc
        }    
    
    def get_operations(self):
        """
        这个函数逻辑用于编辑
        """
        ls=[]
        #if self.permit.changeable_fields():
        ls.append({
            'name':'save','editor':'com-field-op-btn','label':'保存', 'icon': 'fa-save',
        })
        return ls        
    
    def get_heads(self): 
        return []
    
    def get_head_context(self): 
        return {
            'heads':self.get_heads(),
            'ops':self.get_operations(),
            'director_name':self.get_director_name(),
            'extra_mixins':[]  #self.extra_mixins
        }  
    
    def get_tabs(self):
        return []
    
    def get_director_name(self):
        director_name = ''
        for k,v in director.items():
            if v==self.__class__:
                director_name=k
                break
        return director_name     
    

class BaseTabFields(object):
    """标签页form"""
    def __init__(self, *args, **kws): 
        self.row = kws.get('dc')
        self._par_pk = kws.get('pk')
        self.crt_user = kws.get('crt_user')
    
    @classmethod
    def get_director_name(cls): 
        director_name = ''
        for k,v in director.items():
            if v==cls:
                director_name=k
                break
        return director_name
    def is_valid(self): 
        return True
    def save_form(self): 
        self._par_pk = self.row['_par_pk']
        page = CmsPageModel.objects.get(pk = self._par_pk)
        dc = {}
        for k, v in self.row.items():
            if k.startswith('_'):
                continue
            dc[k] = v
        
        page.content = json.dumps(dc)
        page.save()
        
        

    def get_heads(self): 
        return []
    
    def get_operations(self): 
        return [
            { 'name':'save','editor':'com-field-op-btn','label':'保存', 'icon': 'fa-save',}            
        ]
    
    def get_row(self): 
        page = CmsPageModel.objects.get(pk = self._par_pk)
        dc = {
            '_director_name': self.get_director_name(),
            '_par_pk': self._par_pk,
        }
        if page.content:
            dc.update(json.loads(page.content))

        return dc
    