# encoding:utf-8
from __future__ import unicode_literals
from helpers.director.middleware.request_cache import get_request_cache
from django.forms.models import fields_for_model
from django.core import exceptions

class BaseFieldProc(object):
    def __init__(self, instance = None, name = None,model=None): 
        self.instance = instance
        self.name=name
        self.model=model
        
        self.form_field=None
        self.field=None
        
        catch = get_request_cache()
        self.request = catch.get('request')
        self.crt_user= self.request.user
        
    def to_dict(self,inst,name):
        """返回字典
        to_dict 函数会调用这个方法
        """
        return { name :getattr(inst,name)}
    
    def clean_field(self,dc,name):
        """ 
        fields类里，从前端穿过来的row dict数据进行清洗， dc里面有的 字段，才会被调用
        """
        return dc[name]
    
    def dict_table_head(self,head):
        """
        """
        head=self.get_options(head)
        return head 
    
    def dict_field_head(self,head): 
        head = self.get_options(head)      
        return head
    
    def get_options(self,head):
        try:
            if not self.form_field:
                self.form_field = fields_for_model(self.model,fields=[self.name])[self.name]
            if hasattr(self.form_field,'choices'):
                head['editor'] = 'com-table-mapper'
                #head['options'] =  [{'value':x[0],'label':x[1]} for x in self.field.choices]
                catch = get_request_cache()
                options_name = '%(model)s.%(field)s.options'% {'model': model_to_name(self.model) ,'field': head['name']}
                if not catch.get(options_name):
                    def myoption():
                        options=[{'value':val,'label':str(lab)} for val,lab in self.form_field.choices]
                        catch[options_name]=options
                        return options
                    head['options']= myoption  #catch.get(options_name)
                else:
                    head['options']=catch.get(options_name)
        except exceptions.FieldError:
            pass
        return head
    
    
    def filter_get_range_head(self,name,model):
        """
        返回None，则会用默认的
        返回字典 {'name':name,
                'label':_('我的名字'),
                'editor':'com-date-range-filter'
                }
        """
        return {
            'name': name,
            'editor':'com-date-range-filter'
        }
    
    
    def filter_get_head(self,name,model):
        return {'name': name, 'editor': 'com-filter-select', 'options': [],}
    
    
    def filter_adapt_dict(self,dc,name):
        return dc
    
    def filter_clean_filter_arg(self, f_str):
        if f_str == '':
            return  None
        else:
            return f_str

    
    def filter_clean_search(self, q_str):
        if q_str == '':
            return None
        return q_str


def model_to_name(model):
    """
    @model: model or instance
    
    """
    return model._meta.app_label+'.'+model._meta.model_name