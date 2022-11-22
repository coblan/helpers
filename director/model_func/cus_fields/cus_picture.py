# encoding:utf-8
from __future__ import unicode_literals
from django.db import models
from helpers.director.shortcut import field_map
from helpers.director.model_func.field_proc import BaseFieldProc
import re
from django.utils import timezone

class PictureField(models.CharField):
    pass

class PictureProc(BaseFieldProc):
    '''
    接收图片，以md5的形式，存储在public/images,默认folder是head['up_url']='/d/upload?path=public/images'
    如果要自定义，请在dict_head中，重新指定head['up_url']='/d/upload?path=public/{yourfolder}'
    '''

    def clean_field(self,dc,name):
        """
        """
        value = dc.get(name)
        return value

    def dict_table_head(self,head): 
        head['editor']='com-table-picture'
        head['show_tooltip'] = False
        return head
    
    def dict_field_head(self,head):
        head['editor']='com-field-picture'
        #head['up_url']='/d/upload?path=general_upload/images'
        head['up_url']='/d/upload?path=general_upload/images'
        #head['config']={
            #'up_url':'/d/upload?path=public/images'
        #}
        return head

field_map[PictureField]=PictureProc