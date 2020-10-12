
from django.db import models
from helpers.director.shortcut import field_map
from helpers.director.model_func.field_proc import BaseFieldProc
import re
from django.utils.text import Truncator
from helpers.func.html import textify,truncatehtml
from django.utils import timezone
from django.utils.translation import ugettext as _

class MonthField(models.DateField):
    pass

class MonthFieldProc(BaseFieldProc):
    '''
    '''
    
    def to_dict(self, inst, name):
        value = getattr(inst,name,'')
        if value:
            return {
                name:value.strftime('%Y-%m')
            }
        else:
            return {
                name:''
            }
    
    def clean_field(self,dc,name):
        """
        """
        value = dc.get(name)
        if value:
            return timezone.datetime.strptime(value,'%Y-%m')
        else:
            return value

    #def dict_table_head(self,head): 
        #head['editor']='com-table-label-shower'
        #return head
    
    def filter_get_head(self, name, model):
        f = model._meta.get_field(name)
        return {
            'name':name,
            'label':_(f.verbose_name),
            'editor':'com-filter-month',
        }
    
    def filter_clean_filter_arg(self, name, search_args):
        """
        可能情况: {'month': None} {"month":''}
        """
        if name in search_args:
            if  search_args[name] and len(search_args[name]) ==7:
                search_args[name] = search_args[name]+'-01'
            else:
                search_args.pop(name)
        return search_args
    
    def dict_field_head(self,head):
        head['editor']='com-field-month'
        return head

field_map[MonthField]=MonthFieldProc