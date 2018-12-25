# encoding:utf-8
from __future__ import unicode_literals

from ..field_proc  import BaseFieldProc
from django.db.models import CharField
from .. .base_data import field_map
from django.utils.translation import ugettext as _

class CharProc(BaseFieldProc):

    def dict_field_head(self, head): 
        options_head = self.get_options()   
        if options_head:
            head.update(options_head)
            head['editor'] = 'com-field-select'
        else:
            head['editor'] = 'linetext'
        return head    

    def filter_get_range_head(self,name,model):
        f = model._meta.get_field(name)
        return {'name':name,
                'label':_(f.verbose_name),
                'editor':'com-date-range-filter'
                }
    
    def filter_get_head(self, name, model):
        this_field= model._meta.get_field(name)
        if this_field.choices:        
            options = [{'value':x[0],'label':x[1]} for x in this_field.choices]
        else:
            query = model.objects.all().values_list(name,flat=True).distinct()
            #ls = list(query)
            options = [{ 'value':x,'label':str(x)} for x in query]
            
        return {
            'name':name,
            'label':_(this_field.verbose_name),
            'editor':'com-select-filter',
            'options':options
        }


field_map.update({
    CharField:CharProc
})
