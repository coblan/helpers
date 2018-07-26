# encoding:utf-8
from __future__ import unicode_literals

from ..field_proc  import BaseFieldProc
from django.db.models import BooleanField
from .. .base_data import field_map
from django.utils.translation import ugettext as _

class BoolProc(BaseFieldProc):

    #def filter_get_range_head(self,name,model):
        #f = model._meta.get_field(name)
        #return {'name':name,
                #'label':_(f.verbose_name),
                #'editor':'com-date-range-filter'
                #}
    
    #def to_dict(self, inst, name): 
        #value = getattr(inst,name)
        #if not value:
            #return False
        #return bool(value)
    
    def dict_table_head(self, head): 
        head['editor'] = 'com-table-bool-shower'
        return head
    
    def dict_field_head(self, head): 
        head['editor'] = 'bool'
        return head
    
    
    
    def filter_get_head(self, name, model):
        this_field= model._meta.get_field(name)
        if this_field.choices:        
            options = [{'value':x[0],'label':x[1]} for x in this_field.choices]
        else:
            query = model.objects.all().values_list(name,flat=True)
            ls = list(set(query))
            options = [{ 'value':x,'label':str(x)} for x in ls]
            
        return {
            'name':name,
            'label':_(this_field.verbose_name),
            'editor':'com-select-filter',
            'options':options
        }


field_map.update({
    BooleanField:BoolProc
})
