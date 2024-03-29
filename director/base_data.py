import inspect
from django.conf import settings
from helpers.func import ex
import re
# used for model render
page_dc={
    #'xxx_model': {'model':'xxx','table_temp':xxx,'field_temp':xxx}
}

model_dc={
}

permit_list=[]

js_tr_list=[]

js_lib_list= []

director={
}

director_views={
}

field_map={
}


inspect_dict ={
    'page_dc':page_dc,
    'director':director,
    'director_views':director_views,
    'field_map':field_map,
}

from functools import wraps

#doc_dict = {}

#def doc_str(file_key,text,sort=100,tag=['api']):
    #if file_key not in doc_dict:
        #doc_dict[file_key] = []
    #doc_dict[file_key].append(
        #{'text':text,'sort':sort,'tag':tag}
    #)
    

#def doc_fun(file_key,sort=100,tag=['api']):
    #if file_key not in doc_dict:
        #doc_dict[file_key] = []
        
    #def _fun(fun): 
        #doc_dict[file_key].append(
            #{'text':fun.__doc__,'sort':sort,'tag':tag}
        #)
        #@wraps(fun)
        #def _fun2(*args, **kargs): 
            #return fun(*args, **kargs)
        #return _fun2
    #return _fun

director_setting={}

def director_view(name,allow_overlap=False,allow_methods=None): 
    def _fun(fun): 
        #director[name] = fun
        if not allow_overlap:
            if name in director_views:
                raise UserWarning('name=%s的director_view已经存在'%name)
        if allow_methods:
            ex.set_dict_path(director_setting,'%s.methods'%name,allow_methods)
        
        director_views[name] = fun
        @wraps(fun)
        def _fun2(*args, **kargs): 
            return fun(*args, **kargs)
        _fun2.director_name = name
        return _fun2
    return _fun

def director_element(name): 
    def _fun(fun): 
        director[name] = fun
        return fun
        #@wraps(fun)
        #class _ele(fun):
            #pass
        #return _ele
        #def _fun2(*args, **kargs): 
            #return fun(*args, **kargs)
        #return _fun2
    return _fun


def find_director(name:str):
    left_name = name
    if left_name.startswith('/dapi'):
        rt = re.search('/dapi/(.+)',left_name)
        left_name= rt.groups()[0]
    if left_name.startswith('element/'):
        rt2 = re.search('element/(.+)/(\w+)$',left_name)
        left_name= rt2.groups()[0]
        attr_name = rt2.groups()[1]
        Element = director.get(left_name)
        element = Element()
        return getattr(element,attr_name,None)
    else:
        return director.get(name,None)


"""
下面三个item都过时了，现在使用db_router对事务进行控制
"""
director_transaction= {}
def append_transaction(director_name,db_name):
    director_transaction[director_name] = director_transaction.get(director_name)  or list(getattr(settings,'REQUEST_TRANSACTION_DB',['default']))
    if db_name not in director_transaction[director_name]:
        director_transaction[director_name].append(db_name)

director_exclude_transaction= []
def exclude_transaction(fun):
    director_exclude_transaction.append(fun.director_name)
    return fun    
   