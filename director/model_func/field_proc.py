# encoding:utf-8
from __future__ import unicode_literals

class BaseFieldProc(object):
    def to_dict(self,inst,name):
        """返回字典"""
        return { name :getattr(inst,name)}
    
    def clean_field(self,dc,name):
        # dc里面有的 字段，才会被调用
        return dc[name]
    
    #def from_dict(self,value,field) :
        #pass
    
    def dict_table_head(self,head):
        return head
    
    def dict_field_head(self,head):
        return head
    
    def get_range_filter_head(self):
        """
        返回None，则会用默认的
        返回字典 {'name':name,
                'label':_('我的名字'),
                'editor':'com-date-range-filter'
                }
        """
        return None
    