# encoding:utf-8
from __future__ import unicode_literals

from ..field_proc  import BaseFieldProc
from django.db.models import DecimalField
from .. .base_data import field_map

class DecimalProc(BaseFieldProc):
    def to_dict(self,inst,name):
        data = getattr(inst,name)
        return {name:unicode(data)}
    
    def clean_field(self,dc,name):
        return float(dc.get(name))
    
field_map.update({
    DecimalField:DecimalProc
})