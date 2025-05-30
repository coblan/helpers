# encoding:utf-8
from __future__ import unicode_literals
from helpers.director.middleware.request_cache import get_request_cache
from django.forms.models import fields_for_model
from django.core import exceptions

class BaseFieldProc(object):
    def __init__(self, instance = None, name = None,model=None,field = None): 
        self.instance = instance
        self.name=name
        self.model=model
        if not self.model and self.instance:
            self.model = self.instance . __class__
        
        self.form_field=None
        self.field=field
        if not self.field and self.model and name:
            self.field = self.model._meta.get_field(name)
            
        self.request = get_request_cache().get('request')
        self.crt_user= self.request.user
        
    def to_dict(self,inst,name):
        """返回字典
        to_dict 函数会调用这个方法
        """
        value = getattr(inst,name)
        if isinstance(value,str):
            return {name:value.strip()}
        else:
            return { name :value}
    
    def clean_field(self,dc,name):
        """ 
        fields类里，从前端穿过来的row dict数据进行清洗， dc里面有的 字段，才会被调用
        """
        return dc[name]
    
    def dict_table_head(self,head):
        """
        """
        options=self.get_options()
        if options:
            head['options'] = options
            head['editor'] = 'com-table-mapper'
        else:
            head['editor']='com-table-span'
        return head 
    
    def dict_field_head(self,head): 
        options = self.get_options()  
        if options:
            head['options']=options
            head['editor'] = 'com-field-select'
        return head
    
    def get_options(self,query=None):
        options=None
        try:
            if not self.form_field:
                self.form_field = fields_for_model(self.model,fields=[self.name]).get(self.name)
                if not self.form_field:
                    return []
            if hasattr(self.form_field,'choices'):
                #head['options'] =  [{'value':x[0],'label':x[1]} for x in self.field.choices]
                catch = get_request_cache()
                options_name = '%(model)s.%(field)s.options'% {'model': model_to_name(self.model) ,'field': self.name}
                if not catch.get(options_name):
                    def myoption():
                        if query:
                            options = [{'value':self.cleanOption(x.pk),'label':str(x)} for x in query]
                        else:
                            options=[{'value':self.cleanOption(val),'label':str(lab)} for val,lab in self.form_field.choices if val !='']
                        #if self.form_field.required:
                            #options=[{'value':val,'label':str(lab)} for val,lab in self.form_field.choices if val !='']
                        #else:
                            #options=[{'value':None if val=='' else val,'label':str(lab)} for val,lab in self.form_field.choices ]
                        catch[options_name]=options
                        return options
                    options= myoption  #catch.get(options_name)
                else:
                    options=catch.get(options_name)
        except exceptions.FieldError:
            pass
        return options
    
    def cleanOption(self,val):
        if isinstance(val,int):
            if val >2147483647 or val < -2147483648:
                return str(val)
            else:
                return val
        else:
            return val
    
    
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
    
    def filter_clean_filter_arg(self, name,search_args):
        if name not in search_args:
            return search_args
        
        value = search_args.get(name,'')
        if value == '':
            search_args.pop(name)      # 如果是空字符串，就表示不过滤
        elif value is None:
            search_args.pop(name)
            search_args['%s__isnull'%name] = True
        elif isinstance(value,(list,tuple)):
            search_args.pop(name) 
            if value:  # 如果是空数组，就表示不过滤
                search_args['%s__in'%name] = value

        return search_args

    
    def filter_clean_search(self, q_str):
        if q_str == '':
            return None
        return q_str
    
    def filter_inject_sql(self,name,filter_args):    
        if filter_args.get(name) != None and filter_args.get(name) != '':
            '''未完工，需要测试compare 组件功能'''
            compare_name = '_%s_compare'%name
            if compare_name in filter_args:
                cv = str( filter_args.get(compare_name) )
                if cv == '0':
                    return  '%s = %s'%(name,filter_args.get(name) )
                elif cv == '1':
                    return '%s >= %s'%(name,filter_args.get(name) )
                elif cv == '-1':
                    return '%s <= %s'%(name,filter_args.get(name) )
            return '%s = %s'%(name,filter_args.get(name) )
        else:
            return ''
    def cleanDelete(self,name):
        pass


def model_to_name(model):
    """
    @model: model or instance
    
    """
    return model._meta.app_label+'.'+model._meta.model_name