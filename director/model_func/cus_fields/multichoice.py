from django.db.models import CharField,TextField
from .. field_procs.charproc import CharProc
from .. .base_data import field_map
from helpers.director.shortcut import request_cache
from django.utils.translation import ugettext as _

class MultiChoiceField(CharField):
    """
    多选字段，选项由 choices传入，与django的普通字段一致.
    """
    def __init__(self, *args, **kwargs):
        self.my_choices = kwargs.pop('choices',[])
        self.seperator = kwargs.pop('seperator',',')
        self.full_choice = kwargs.pop('full_choice',None)
        super().__init__(*args,**kwargs)
    
class MultiChoiceTextField(TextField):
    """
    多选字段，选项由 choices传入，与django的普通字段一致.
    """
    def __init__(self, *args, **kwargs):
        choices = kwargs.pop('choices',[])
        if callable(choices):
            self.my_choices = choices()
        else:
            self.my_choices = choices
        self.seperator = kwargs.pop('seperator',',')
        self.full_choice = kwargs.pop('full_choice',None)
        self.data_type=kwargs.pop('data_type',int)
        super().__init__(*args,**kwargs)
        

class MultiChoiceProc(CharProc):
    def to_dict(self, inst, name):
        seperator = self.field.seperator
        value = getattr(inst,name)
        if not value:
            return {name:[]}
        
        if self.field.full_choice and value == self.field.full_choice:
            ls = [x[0] for x in self.field.my_choices]
        else:
            ls = [x for x in value.split(seperator) if x!=''] 
        try:
            if self.field.data_type==int:
                ls = [ int(x) for x in ls]
        except ValueError:
            pass
        
        return { name :ls}
    
    def clean_field(self, dc, name):
        seperator = self.field.seperator
        if isinstance(dc[name],str):
            myvalue = [x for x in dc[name].split(seperator) if x]
        else:
            myvalue = dc[name]
        myvalue = [ str(x) for x in myvalue]
        if self.field.full_choice :
            whole_values = [str( x[0] ) for x in self.field.my_choices]
            for x in whole_values:
                if not x in myvalue:
                    return seperator.join( [str(x) for x in myvalue])
            return self.field.full_choice
        else:
            return  seperator.join( [str(x) for x in myvalue])
    
    def dict_table_head(self, head):
        head['editor']='com-table-array-mapper'
        head['options'] = self.get_options()
        return head
    
    def dict_field_head(self, head):
        #head['editor'] = 'com-field-multi-chosen'
        #head['editor'] = 'com-field-multi-select2'
        head['editor'] = 'com-field-select'
        head['multiple'] =True
        if self.field.full_choice != None:
            head['full_choice'] = self.field.full_choice
        head['options'] = self.get_options()
        return head
    
    def get_options(self):
        dc = dict(self.field.my_choices)
        out_list = []
        for k,v in dc.items():
            out_list.append({'value':k,'label':v})
        return out_list
    
    def filter_get_head(self, name, model):
        ".. Note:: 在没有choices的情况下，可能会造成性能问题"
        this_field= model._meta.get_field(name)
        return {
            'name':name,
            'label':_(this_field.verbose_name),
            'editor':'com-filter-select',
            'options':self.get_options()
        }    
    
    
field_map[MultiChoiceField]=MultiChoiceProc
field_map[MultiChoiceTextField]=MultiChoiceProc