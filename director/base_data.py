import inspect

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
}

from functools import wraps

doc_dict = {}

def doc_str(file_key,text,sort=100,tag=['api']):
    if file_key not in doc_dict:
        doc_dict[file_key] = []
    doc_dict[file_key].append(
        {'text':text,'sort':sort,'tag':tag}
    )
    

def doc_fun(file_key,sort=100,tag=['api']):
    if file_key not in doc_dict:
        doc_dict[file_key] = []
        
    def _fun(fun): 
        doc_dict[file_key].append(
            {'text':fun.__doc__,'sort':sort,'tag':tag}
        )
        @wraps(fun)
        def _fun2(*args, **kargs): 
            return fun(*args, **kargs)
        return _fun2
    return _fun



def director_view(name): 
    def _fun(fun): 
        #director[name] = fun
        director_views[name] = fun
        @wraps(fun)
        def _fun2(*args, **kargs): 
            return fun(*args, **kargs)
        return _fun2
    return _fun

def director_element(name): 
    def _fun(fun): 
        director[name] = fun
        @wraps(fun)
        def _fun2(*args, **kargs): 
            return fun(*args, **kargs)
        return _fun2
    return _fun
