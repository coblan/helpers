
from django.db import models
from helpers.director.shortcut import field_map
from helpers.director.model_func.field_proc import BaseFieldProc
import re
from django.utils.text import Truncator
import logging
general_log = logging.getLogger('general_log')
from helpers.func.url_path import media_url_to_path
import os

class PlainFileField(models.CharField):
    def __init__(self,accept='',delete_before_row=False, **kwargs): 
        super().__init__( **kwargs)
        self.delete_before_row=delete_before_row
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
            'upload_url':'/d/upload?director=big-file-saver&split=date', 
           #'media\public\activity'
            #'upload_url':reverse('app_pkg_upload')
        }         
        return head
    
    def cleanDelete(self, name):
        try:
            if self.field.delete_before_row:
                file_url = getattr(self.instance,name)
                if file_url.startswith('/media/'):
                    file_path = media_url_to_path(file_url)
                    if os.path.exists(file_path):
                        os.remove(file_path)
                        general_log.debug(f'delete file {file_url}')
        except Exception as e:
            general_log.warning(str(e))
    

field_map[PlainFileField]=PlainFileProc