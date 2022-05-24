class DotObj(object):
    def __init__(self,dc):
        for k,v in dc.items():
            setattr(self,k,v)
    def __getattr__(self,name):
        try:
            return object.__getattr__(self,name)
        except AttributeError:
            return ''

def read_dict_path(dict_obj,path,default=None):
    ls = path.split('.')
    tmp = dict_obj
    for key in ls:
        if not isinstance(tmp,dict):
            tmp = getattr(tmp,key)  
        else:
            tmp = tmp.get(key,None)
        if tmp == None:
            break
    if tmp == None:
        return default
    else:
        return tmp