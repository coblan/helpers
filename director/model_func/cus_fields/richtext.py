
from django.db import models
from helpers.director.shortcut import field_map
from helpers.director.model_func.field_proc import BaseFieldProc
import re
from django.utils.text import Truncator

class RichtextField(models.TextField):
    pass

class RichtextProc(BaseFieldProc):
    '''
    '''
    
    def to_dict(self, inst, name):
        value = getattr(inst,name,'')
        return {
            name:value,
            '_%s_label'%name:Truncator(value).chars(20, html=True)
        }
    
    def clean_field(self,dc,name):
        """
        """
        value = dc.get(name)
        return value

    def dict_table_head(self,head): 
        head['editor']='com-table-label-shower'
        return head
    
    def dict_field_head(self,head):
        head['editor']='com-field-richtext'
        return head

field_map[RichtextField]=RichtextProc