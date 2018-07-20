from ..field_proc  import BaseFieldProc

from .. .base_data import field_map

class DotStrArrayProc(BaseFieldProc):
    
    def to_dict(self, inst, name): 
        value =  getattr(inst,name)
        if value:
            return { name : value.split(',')}
        else:
            return super().to_dict(inst, name)
    
    def clean_field(self, dc, name): 
        value =  dc[name]
        outstr =  ','.join(value)
        return outstr
    
    def dict_table_head(self, head): 
        """
        options 在 modeltable类的dict_head方法里面去设置
        """
        head['editor'] = 'com-table-array-mapper'
        #head['parse_input'] = 'dotSplit'
        return head
    
    def dict_field_head(self, head): 
        """
        options 在 modelfields类的dict_head方法里面去设置
        """
        head['editor'] = 'field_multi_chosen'
        head['options'] = []
        return head
    
    
