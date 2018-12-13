from django.db.models import DecimalField
from ..field_proc  import BaseFieldProc
from decimal import Decimal
from .. .base_data import field_map

class CusDecimalField(DecimalField):
    def __init__(self, verbose_name=None, name=None, max_digits=None, decimal_places=None, **kwargs): 
        self.digits = kwargs.pop('digits', 2)
        
        super().__init__(verbose_name, name, max_digits, decimal_places, **kwargs)


class CusDecimalProc(BaseFieldProc):
    
    def to_dict(self,inst,name):
        data = getattr(inst,name)
        field = inst.__class__._meta.get_field(name)
        if data:
            return {name: str(round(data, field.digits) )}
        else:
            return {name: 0}
    
    def dict_field_head(self, head):
        name = head['name']
        field = self.instance.__class__._meta.get_field(name)
        head['fv_rule'] = 'digit(%s)' % field.digits
        head['editor'] = 'number'
        return head
        
    
    def clean_field(self,dc,name):
        if dc.get(name):
            return Decimal(dc.get(name))
        else:
            return dc.get(name)
    
field_map.update({
    CusDecimalField:CusDecimalProc
})