from django.shortcuts import render
from helpers.director.shortcut import director
from .models import CmsPageModel
import json

class BasePage(object):
    def __init__(self, request = None,dc = {},crt_user= None , *args, **kwargs): 
        self.request = request
        self.row = dict(dc)
    
    def is_valid(self): 
        return True
    
    def get_row(self): 
        return self.pure_row
    
    def save_form(self): 
        page = CmsPageModel.objects.get(pk = self.row['_page'])
        self.pure_row = {k: v for k, v in self.row.items() if not k.startswith('_')}
        page.content = json.dumps(self.pure_row)
        page.save()
    
    def render(self, par_ctx): 
        template = self.getTemplate()
        ctx = dict(par_ctx)
        ctx.update(self.getContext())
        return render(self.request, template, context= ctx)
    
    def getTemplate(self): 
        return ''
    
    
    def getContext(self): 
        """
        这个函数逻辑，用于显示
        """
        return {}
    
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
    