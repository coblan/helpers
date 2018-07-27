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
        return {}
    
    @classmethod
    def get_operations(cls):
        ls=[]
        #if self.permit.changeable_fields():
        ls.append({
            'name':'save','editor':'com-field-op-btn','label':'保存', 'icon': 'fa-save',
        })
        return ls        
    
    @classmethod
    def get_heads(cls): 
        return []
    
    @classmethod
    def get_head_context(cls): 
        return {
            'heads':cls.get_heads(),
            'ops':cls.get_operations(),
            'director_name':cls.get_director_name(),
            'extra_mixins':[]  #self.extra_mixins
        }  
    
    @classmethod
    def get_director_name(cls):
        director_name = ''
        for k,v in director.items():
            if v==cls:
                director_name=k
                break
        return director_name     
    
    
    