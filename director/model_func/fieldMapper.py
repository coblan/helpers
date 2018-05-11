class BasicMapper(object):
    def to_dict(self,inst,name):
        return inst.name
    
    def clean_field(self,dc,name):
        return {}
    
    def get_label(self,inst,name):
        return None
    
    def dict_table_head(self,head):
        return head
    
    def dict_field_head(self,head):
        return head
    