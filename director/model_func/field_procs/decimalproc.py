# encoding:utf-8
from __future__ import unicode_literals

from ..field_proc  import BaseFieldProc
from django.db.models import DecimalField
from .. .base_data import field_map
from decimal import Decimal


class DecimalProc(BaseFieldProc):
    #digit=2
    #def to_dict(self,inst,name):
        #data = getattr(inst,name)
        #if data is None:
            #return {name: None,}
        #else:
            #return {name:str(round(data,self.digit))}
    
    def clean_field(self,dc,name):
        if dc.get(name): 
            return Decimal(dc.get(name))
        else:
            return Decimal(0)
    
    def dict_field_head(self,head):   
        head['editor'] = 'com-field-number'
        head['fv_rule']='digit(%s)'%self.field.decimal_places
        return head    
    
field_map.update({
    DecimalField:DecimalProc,
    
})