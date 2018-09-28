from django.db.models import IntegerField
from ..field_proc  import BaseFieldProc
from decimal import Decimal
from .. .base_data import field_map
from helpers.director.middleware.request_cache import get_request_cache

class CreateUser(IntegerField):
    pass
    #def __init__(self, verbose_name=None, name=None, max_digits=None, decimal_places=None, **kwargs): 
        #self.digits = kwargs.pop('digits', 2)
        
        #super().__init__(verbose_name, name, max_digits, decimal_places, **kwargs)


class CreateUserProc(BaseFieldProc):
    
    def to_dict(self,inst,name):
        data = getattr(inst,name)
        field = inst.__class__._meta.get_field(name)
        if data:
            return {name: str(round(data, field.digits) )}
        else:
            return {name: ''}
    
    def clean_field(self,dc,name):
        if dc.get(name):
            return Decimal(dc.get(name))
        else:
            return dc.get(name)
    
field_map.update({
    CreateUser:CreateUserProc
})