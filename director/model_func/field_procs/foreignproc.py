from ..field_proc  import BaseFieldProc
from django.db.models import ForeignKey
from .. .base_data import field_map
from django.utils.translation import ugettext as _
from ..dictfy  import model_to_name

class ForeignProc(BaseFieldProc):
    def to_dict(self,inst,name):
        foreign=getattr(inst,name,None)
        if foreign:
            return {
                name:foreign.pk,
                '_%s_model'%name:model_to_name(foreign.__class__),
                '_%s_label'%name:str(foreign)
            }
        else:
            return {}
    
    def clean_field(self,dc,name):
        model = name_to_model( dc.get('_%s_model'%name) )
        return model.objects.get(pk=dc.get(name))     
    
    def filter_get_head(self, name, model):
        this_field= self.model._meta.get_field(name)
        ls=this_field.get_choices()
        ls=ls[1:]
        options= [{'value':x[0],'label':x[1]} for x in ls]       
        return {
            'name':name,
            'label':_(this_field.verbose_name),
            'options':options
        }        


field_map.update({
    ForeignKey:ForeignProc
})