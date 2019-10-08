# encoding:utf-8
from __future__ import unicode_literals

from ..field_proc  import BaseFieldProc
from django.db.models import TextField
from .. .base_data import field_map
from django.utils.translation import ugettext as _

class TextProc(BaseFieldProc):

    def dict_field_head(self, head): 
        head['editor'] = 'com-field-blocktext'
        return head    


    def filter_get_head(self, name, model):
        this_field= model._meta.get_field(name)
        #if this_field.choices:        
            #options = [{'value':x[0],'label':x[1]} for x in this_field.choices]
        #else:
            #query = model.objects.all().values_list(name,flat=True).distinct()
            ##ls = list(query)
            #options = [{ 'value':x,'label':str(x)} for x in query]
            
        return {
            'name':name,
            'placeholder':_(this_field.verbose_name),
            'editor':'com-filter-text',
            #'options':options
        }


field_map.update({
    TextField:TextProc
})
