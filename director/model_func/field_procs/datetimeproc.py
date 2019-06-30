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
            return {
                name: '',
            }
        
    def clean_field(self, dc, name):
        if dc[name]:
            value = dc[name][0:19]
            return timezone.datetime.strptime(value,'%Y-%m-%d %H:%M:%S')
        else:
            return dc[name]
    
    def dict_field_head(self, head):
        head['editor']='com-field-datetime'
        return head
    
    def dict_table_head(self, head):
        head = super().dict_table_head(head)
        head['width'] = 140
        return head
        
    def filter_get_range_head(self,name,model):
        f = model._meta.get_field(name)
        return {'name':name,
                'label':_(f.verbose_name),
                'editor': 'com-date-datetimefield-range-filter'#'com-date-range-filter'
                }
    
    def filter_clean_filter_arg(self, name,search_args):
        v= search_args.get('%s__lte'%name)
        if v and len(v) ==10:
            v+= ' 23:59:59'
            return {'%s__lte'%name:v}
        else:
            return super().filter_clean_filter_arg(name,search_args)

    
    def _filter_dict_query_args(self, dc, name):
        """
        * 这个函数无用了，现在用date 筛选datetime的 23:59:59问题，交由前端控件去补齐去了。*
        普通情况下，都是按照天对时间进行筛选，所以尽管是datetime字段，但是
        datetime  按照天选择
        """
        #end_name = '_end_%s'%name
        end_str = '%s__lte'%name
        if dc.get(end_str):
            dd = timezone.datetime.strptime(dc[end_str],'%Y-%m-%d') 
            sp_one_day = timezone.timedelta(days=1)
            sp_1_s = timezone.timedelta(seconds = 1)
            real_end = dd+sp_one_day - sp_1_s
            return {
                end_str:real_end  #.strftime('%Y-%m-%d')
            }
        else:
            return {}
    

field_map.update({
    DateTimeField:DateTimeProc
})
