# encoding:utf-8
from __future__ import unicode_literals

from ..field_proc  import BaseFieldProc
from django.db.models import DateField
from .. .base_data import field_map
from django.utils.translation import ugettext as _

class DateProc(BaseFieldProc):
    def to_dict(self,inst,name):
        date=getattr(inst,name)
        if date:
            return {name:date.isoformat()}
        else:
            return {}
        
    def filter_get_range_head(self,name,model):
        f = model._meta.get_field(name)
        return {'name':name,
                'label':_(f.verbose_name),
                'editor':'com-date-range-filter'
                }

field_map.update({
    DateField:DateProc
})
    