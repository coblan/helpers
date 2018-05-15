# encoding:utf-8
from __future__ import unicode_literals

class BasicMapper(object):
    def to_dict(self,inst,name):
        return inst.name
    
    def clean_field(self,dc,name):
        # dc里面有的 字段，才会被调用
        return dc[name]
    
    def from_dict(self,value,field) :
        pass
    
    def dict_table_head(self,head):
        return head
    
    def dict_field_head(self,head):
        return head
    