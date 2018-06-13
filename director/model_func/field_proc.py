# encoding:utf-8
from __future__ import unicode_literals

class BaseFieldProc(object):
    def to_dict(self,inst,name):
        """返回字典"""
        return { name :getattr(inst,name)}
    
    def clean_field(self,dc,name):
        # dc里面有的 字段，才会被调用
        return dc[name]
    
    def dict_table_head(self,head):
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
        return {}
    
    def filter_get_head(self,name,model):
        return {}
    
    
    def filter_adapt_dict(self,dc,name):
        return dc
    
    def filter_dict_query_args(self,dc,name):
        return {}
    