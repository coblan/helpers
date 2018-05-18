# encoding:utf-8
from __future__ import unicode_literals

from ..field_proc  import BaseFieldProc
from django.db.models import DateTimeField
from .. .base_data import field_map
from django.utils.translation import ugettext as _
from django.utils import timezone

class DateTimeProc(BaseFieldProc):
    def to_dict(self,inst,name):
        value = getattr(inst,name,None)
        if value:
            return {
                name:value.strftime('%Y-%m-%d %H:%M:%S')
                }
        else:
            return {}
        
    def clean_field(self, dc, name):
        if dc[name]:
            return timezone.datetime.strptime(dc[name],'%Y-%m-%d %H:%M:%S')
        else:
            return dc[name]
        
    def filter_get_range_head(self,name,model):
        f = model._meta.get_field(name)
        return {'name':name,
                'label':_(f.verbose_name),
                'editor':'com-date-range-filter'
                }
    
    def filter_dict_query_args(self, dc, name):
        #end_name = '_end_%s'%name
        end_str = '%s__lte'%name
        if dc.get(end_str):
            dd = timezone.datetime.strptime(dc[end_str],'%Y-%m-%d') 
            sp_one_day = timezone.timedelta(days=1)
            real_end = dd+sp_one_day
            return {
                end_str:real_end.strftime('%Y-%m-%d')
            }
        else:
            return {}
    

field_map.update({
    DateTimeField:DateTimeProc
})
