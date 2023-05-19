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
            tmp = getattr(tmp,key,None)  
        else:
            tmp = tmp.get(key,None)
        if tmp == None:
            break
    if tmp == None:
        return default
    else:
        return tmp

def set_dict_path(dc,path,value):
    ls = path.split('.')
    last = dc
    for index,key in enumerate(ls):
        if key not in last :
            last[key] ={}
        if index < len(ls)-1:
            last = last[key]
        else:
            last[key] = value


def dict_pop(dc,name):
    if name in dc:
        return dc.pop(name)
    else:
        return None