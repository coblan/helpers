from ..field_proc  import BaseFieldProc
from django.db.models import ManyToManyField
from .. .base_data import field_map
from django.utils.translation import gettext as _
from helpers.director.shortcut import get_request_cache
from ..dictfy  import model_to_name,name_to_model

class ManyProc(BaseFieldProc):
    def to_dict(self,inst,name):
        out =[]
        if inst.pk:
            for item in getattr(getattr(inst,name),'all')():
                out.append(item.pk)
                
        return {
            name:out
            }
    
    
    def dict_field_head(self,head):  
        options = self.get_options()   
        #head['editor'] = 'com-field-multi-chosen'
        head['editor'] = 'com-field-multi-select2'
        head['options'] = options
        return head 
    
    def dict_table_head(self,head):
        """
        """
        options = self.get_options() 
        head['editor'] = 'com-table-array-mapper'
        head['options'] = options
        return head
    
    def filter_get_head(self,name,model):
        options = self.get_options()   
        this_field= model._meta.get_field(name)
        return {'name': name, 
                'editor': 'com-filter-search-select',
                'label':_(this_field.verbose_name),
                'options': options,}    
       

field_map.update({
    ManyToManyField:ManyProc
})