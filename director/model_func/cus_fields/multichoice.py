from django.db.models import CharField
from .. field_procs.charproc import CharProc
from .. .base_data import field_map
from helpers.director.shortcut import request_cache

class MultiChoiceField(CharField):
    """
    多选字段，选项由 choices传入，与django的普通字段一致.
    """
    def __init__(self, *args, **kwargs):
        self.my_choices = kwargs.pop('choices',[])
        self.seperator = kwargs.pop('seperator',';')
        self.full_choice = kwargs.pop('full_choice',None)
        super().__init__(*args,**kwargs)

class MultiChoiceProc(CharProc):
    def to_dict(self, inst, name):
        seperator = self.field.seperator
        value = getattr(inst,name)
        if self.field.full_choice and value == self.field.full_choice:
            options = self.get_options()
            ls = [x['value'] for x in options]
        else:
            ls = [x for x in value.split(seperator) if x!=''] 
        return { name :ls}
    
    def clean_field(self, dc, name):
        seperator = self.field.seperator
        if self.field.full_choice :
            options= self.get_options()
            option_list = [x['value'] for x in options]
            for x in options:
                if not x['value'] in dc[name]:
                    return seperator.join( dc[name])
            return self.field.full_choice
        else:
            return  seperator.join( dc[name])
    
    def dict_table_head(self, head):
        head['editor']='com-table-array-mapper'
        head['options'] = self.get_options()
        return head
    
    def dict_field_head(self, head):
        head['editor'] = 'com-field-multi-chosen'
        head['editor'] = 'com-field-multi-select2'
        head['options'] = self.get_options()
        return head
    
    def get_options(self):
        dc = dict(self.field.my_choices)
        out_list = []
        for k,v in dc.items():
            out_list.append({'value':k,'label':v})
        return out_list
    
field_map[MultiChoiceField]=MultiChoiceProc