from ..field_proc  import BaseFieldProc
from django.db.models import NullBooleanField
from .. .base_data import field_map


class NullBoolProc(BaseFieldProc):

    def dict_table_head(self, head): 
        head['editor'] = 'com-table-bool-shower'
        return head
    
    def dict_field_head(self, head): 
        head['editor'] = 'com-field-select'
        head['options']=[
            {'value':None,'label':'空'},
            {'value': True, 'label': '是',}, 
            {'value': False, 'label': '否',},
        ]

        return head
       
    
    def filter_get_head(self, name, model):
        this_field= model._meta.get_field(name)
        options = [
            {'value':None,'label':'空'},
            {'value': True, 'label': '是',}, 
            {'value': False, 'label': '否',},
        ]
   
        return {
            'name':name,
            'label':this_field.verbose_name,
            'editor':'com-select-filter',
            'options':options
        }


field_map.update({
    NullBooleanField:NullBoolProc
})
