# encoding:utf-8
from __future__ import unicode_literals

from ..field_proc  import BaseFieldProc
from django.db.models import DecimalField
from .. .base_data import field_map
from decimal import Decimal

class DecimalProc(BaseFieldProc):
    digit=2
    def to_dict(self,inst,name):
        data = getattr(inst,name)
        if not data and data !=0:
            return {name: data,}
        else:
            return {name:str(round(data,self.digit))}
    
    def clean_field(self,dc,name):
        if dc.get(name) or dc.get(name) ==0: 
            return Decimal(dc.get(name))
        else:
            return dc.get(name)
    
    def dict_field_head(self,head):   
        head['editor'] = 'com-field-number'
        head['fv_rule']='digit(%s)'%self.digit
        return head    
    
field_map.update({
    DecimalField:DecimalProc,
    
})