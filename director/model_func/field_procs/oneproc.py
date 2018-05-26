
from ..field_proc  import BaseFieldProc
from django.db.models import OneToOneField
from .. .base_data import field_map
from ..dictfy import model_to_name


class OneProc(BaseFieldProc):
    def to_dict(self,inst,name):
        foreign=getattr(inst,name,None)
        if foreign:
            return {
                name: foreign.pk ,
                '_%s_model'%name:model_to_name(foreign.__class__)
            }
        else:
            return {}
    
    def clean_field(self,dc,name):
        model = name_to_model( dc.get('_%s_model'%name) )
        return model.objects.get(pk=dc.get(name))  
    
    
field_map.update({
    OneToOneField:OneProc
})