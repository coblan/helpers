from django.db.models import CharField
from .. field_procs.charproc import CharProc
from .. .base_data import field_map

class MultiChoiceField(CharField):
    """
    多选字段，选项由 choices传入，与django的普通字段一致.
    """
    def __init__(self, *args, **kwargs):
        self.my_choices = kwargs.pop('choices',[])
        super().__init__(*args,**kwargs)

class MultiChoiceProc(CharProc):
    def to_dict(self, inst, name):
        value = getattr(inst,name)
        ls = value.split(';')
        return { name :ls}
    
    def clean_field(self, dc, name):
        return  ';'.join( dc[name])
    
    def dict_table_head(self, head):
        head['editor']='com-table-array-shower'
        head['options'] = self.get_options()
        return head
    
    def dict_field_head(self, head):
        head['editor'] = 'com-field-multi-chosen'
        head['options'] = self.get_options()
        return head
    
    def get_options(self):
        field = self.model._meta.get_field(self.name)
        dc = dict(field.my_choices)
        out_list = []
        for k,v in dc.items():
            out_list.append({'value':k,'label':v})
        return out_list
    
field_map[MultiChoiceField]=MultiChoiceProc