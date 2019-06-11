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

field_map={
}
site_cfg = {
}

def director_view(name): 
    def _fun(fun): 
        director[name] = fun
        def _fun2(*args, **kargs): 
            return fun(*args, **kargs)
        return _fun2
    return _fun

