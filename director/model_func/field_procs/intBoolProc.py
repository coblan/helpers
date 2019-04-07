from . boolproc import BoolProc

class IntBoolProc(BoolProc):
    def to_dict(self, inst, name): 
        value = getattr(inst,name)
        return {name: bool(value)}
    
    def clean_field(self, dc, name): 
        value = dc[name]
        return 1 if value else 0
