from django.db.models import DateTimeField,DateField
from ..field_procs.datetimeproc import DateTimeProc
from .. .base_data import field_map

class FormDatetime(DateTimeField):
    def __init__(self, verbose_name=None, name=None, auto_now=False,
                     auto_now_add=False, **kwargs):
        self.auto_now, self.auto_now_add = auto_now, auto_now_add
        if auto_now or auto_now_add:
            #kwargs['editable'] = False
            kwargs['blank'] = True
        super(DateField, self).__init__(verbose_name, name, **kwargs)


class FormDatetimeProc(DateTimeProc):
    pass

field_map[FormDatetime] = FormDatetimeProc