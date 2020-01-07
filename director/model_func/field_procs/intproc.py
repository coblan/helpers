# encoding:utf-8
from __future__ import unicode_literals
import re
from ..field_proc  import BaseFieldProc
from django.db.models import IntegerField, SmallIntegerField,BigIntegerField
from .. .base_data import field_map,validator_map
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
        valid_rules = [ validator_map.get( validator.__name__ ,None) for validator in self.field.validators ]
        valid_rules =[x for x in valid_rules if x]
        if options:
            head['options']=options
            head['editor'] = 'com-field-select'
        else:
            head['editor'] = 'com-field-number'
            valid_rules.append('integer')
            head['fv_rule'] = ';'.join(valid_rules)
            
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
            'editor':'com-filter-select',
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


class BigProc(IntProc):
    def filter_clean_search(self, q_str): 
        if re.search('^\d+$', q_str):
            bb= int(q_str)
            if (-10**19 +1 < bb < 10**19 -1 ):
                return bb
            else:
                return None

        else:
            return None

field_map.update({
    IntegerField:IntProc, 
    SmallIntegerField: IntProc,
    BigIntegerField:BigProc,
})
