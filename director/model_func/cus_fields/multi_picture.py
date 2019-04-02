# encoding:utf-8
from __future__ import unicode_literals
from django.db import models
from helpers.director.shortcut import field_map
from helpers.director.model_func.field_proc import BaseFieldProc
import re

class MultiPictureField(models.TextField):
    pass

class MultiPictureProc(BaseFieldProc):
    '''
    接收图片，以md5的形式，存储在public/images,默认folder是head['up_url']='/d/upload?path=public/images'
    如果要自定义，请在dict_head中，重新指定head['up_url']='/d/upload?path=public/{yourfolder}'
    '''
    def to_dict(self, inst, name):
        value = getattr(inst,name,None)
        if not value:
            out_value=[]
        else:
            out_value=value.split(',')
        
        return {
            name:out_value,
        }
    
    def dict_table_head(self, head):
        head['editor'] = 'com-table-multi-image'
        head['show_tooltip'] = False
        return head
    
    def clean_field(self,dc,name):
        """
        """
        value = dc.get(name)
        return ','.join(value)
    
    def dict_field_head(self,head):
        head['editor']='com-field-multi-picture'
        head['up_url']='/d/upload?path=general_upload/images'
        
        return head

field_map[MultiPictureField]=MultiPictureProc