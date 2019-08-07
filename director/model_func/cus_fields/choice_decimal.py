from django.db.models import DecimalField
from ..field_proc  import BaseFieldProc
from decimal import Decimal
from .. .base_data import field_map

class ChoiceDecimalField(DecimalField):
    "可以选择的Decimal"
    def __init__(self, verbose_name=None, name=None, max_digits=None, decimal_places=None, **kwargs): 
        if 'choices' in kwargs:
            self.choice = kwargs.pop('choices')
        super().__init__(verbose_name, name, max_digits, decimal_places, **kwargs)


class ChoiceDecimalProc(BaseFieldProc):
    
    #def to_dict(self,inst,name):
        #data = getattr(inst,name)
        #if data:
            #return { name: str(data)}
        #else:
            #return {name:data}
    
    def dict_table_head(self, head):
        head['editor'] = 'com-table-mapper'
        head['options'] = self.get_options()
    
    def dict_field_head(self, head):
        name = head['name']
        field = self.instance.__class__._meta.get_field(name)
        head.update({
            'editor':'com-field-select',
            'options':[{'value':x[0],'label':x[1]} for x in field.choice]
        })
        return head
    
    def get_options(self):
        return [{'value':x[0],'label':x[1]} for x in self.field.choice]
    
    def clean_field(self,dc,name):
        if dc.get(name):
            return Decimal(dc.get(name))
        else:
            return dc.get(name)
    
field_map.update({
    ChoiceDecimalField:ChoiceDecimalProc
})