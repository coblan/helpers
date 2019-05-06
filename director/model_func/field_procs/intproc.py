# encoding:utf-8
from __future__ import unicode_literals
import re
from ..field_proc  import BaseFieldProc
from django.db.models import IntegerField, SmallIntegerField,BigIntegerField
from .. .base_data import field_map
from django.utils.translation import ugettext as _

class IntProc(BaseFieldProc):

    def filter_get_range_head(self,name,model):
        f = model._meta.get_field(name)
        return {'name':name,
                'label':_(f.verbose_name),
                'editor':'com-date-range-filter'
                }

    def dict_field_head(self, head): 
        options = self.get_options()   
        if options:
            head['options']=options
            head['editor'] = 'com-field-select'
    
        #if hasattr(self.field, 'choices'): 
            #head['editor'] = 'sim_select'
            ##options = [{'value':x[0],'label':x[1]} for x in self.field.choices]
            ##head['options'] = options
        else:
            head['editor'] = 'number'
            head['fv_rule'] = 'range(-2147483648~2147483647)'
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
    
    def filter_clean_search(self, q_str): 
        if re.search('^\d+$', q_str):
            bb= int(q_str)
            if -2147483648 < bb <2147483647:
                return bb
            else:
                return None
        else:
            return None


field_map.update({
    IntegerField:IntProc, 
    SmallIntegerField: IntProc,
    BigIntegerField:IntProc,
})
