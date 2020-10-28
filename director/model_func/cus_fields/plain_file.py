
from django.db import models
from helpers.director.shortcut import field_map
from helpers.director.model_func.field_proc import BaseFieldProc
import re
from django.utils.text import Truncator

class PlainFileField(models.CharField):
    def __init__(self,accept='', **kwargs): 
        super().__init__( **kwargs)
        self.accept = accept

class PlainFileProc(BaseFieldProc):
    '''
    '''
    def clean_field(self,dc,name):
        """
        """
        value = dc.get(name)
        return value

    def dict_table_head(self,head): 
        head['editor']='com-table-link'
        return head
    
    def dict_field_head(self,head):
        head['editor']='com-field-plain-file'
        head['config']={
            #'multiple':False,
            'accept':self.field.accept,
            #'upload_url':'/d/upload?path=public/activity', 
           #'media\public\activity'
            #'upload_url':reverse('app_pkg_upload')
        }         
        return head

field_map[PlainFileField]=PlainFileProc