# encoding:utf-8
from __future__ import unicode_literals

class BaseFieldProc(object):
    def __init__(self, instance = None, field = None): 
        self.instance = instance
        self.field = field
        
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
        if self.field.choices:
            head['editor'] = 'com-table-mapper'
            #head['options'] =  [{'value':x[0],'label':x[1]} for x in self.field.choices]
        return head 
    
    def dict_field_head(self,head):     
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
    