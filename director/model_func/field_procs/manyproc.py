from ..field_proc  import BaseFieldProc
from django.db.models import ManyToManyField
from .. .base_data import field_map

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
        head['editor'] = 'com-field-multi-chosen'
        head['options'] = options
        return head 
    
    def dict_table_head(self,head):
        """
        """
        options = self.get_options() 
        head['editor'] = 'com-table-array-mapper'
        head['options'] = options
        return head
       

field_map.update({
    ManyToManyField:ManyProc
})