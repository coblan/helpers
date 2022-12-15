
from ..field_proc  import BaseFieldProc
from django.db.models import OneToOneField
from .. .base_data import field_map
from ..dictfy import model_to_name, name_to_model
from . foreignproc import ForeignProc

#class OneProc(BaseFieldProc):
class OneProc(ForeignProc):
    def to_dict(self,inst,name):
        
        foreign=getattr(inst,name,None)
        if foreign:
            return {
                name: foreign.pk ,
                '_%s_model'%name:model_to_name(foreign.__class__), 
                '_%s_label'%name:str(foreign), 
            }
        else:
            related_model = inst.__class__._meta.get_field(name).related_model
            return {
                name:None,
                '_%s_label'%name:'', 
                '_%s_model'%name:model_to_name(related_model)
            }
    
    def get_options(self):
        if getattr(self.field.target_field.model,'bigdata',False):
            return [{'value':1,'label':'大数据量,请自定义'}]        
        else:
            return super().get_options()
        
    def dict_table_head(self, head):
        head['options']=[]
        head['editor'] = 'com-table-label-shower'
        return head
    
    #def clean_field(self,dc,name):
        #model = name_to_model( dc.get('_%s_model'%name) )
        #return model.objects.get(pk=dc.get(name))  
    
    
field_map.update({
    OneToOneField:OneProc
})