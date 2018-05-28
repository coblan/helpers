# encoding:utf-8
from __future__ import unicode_literals

from ..field_proc  import BaseFieldProc
from django.db.models import DecimalField
from .. .base_data import field_map
from decimal import Decimal

class DecimalProc(BaseFieldProc):
    def to_dict(self,inst,name):
        data = getattr(inst,name)
        return {name:str(data)}
    
    def clean_field(self,dc,name):
        return Decimal(dc.get(name))
    
field_map.update({
    DecimalField:DecimalProc
})