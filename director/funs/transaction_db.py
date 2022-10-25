import inspect
from helpers.director.base_data import director,director_views
from django.conf import settings
from helpers.func.d_import import import_element
if getattr(settings,'DATABASE_ROUTERS'):
    router_str = getattr(settings,'DATABASE_ROUTERS')[0]
    routerCls = import_element(router_str)
    router = routerCls()
else:
    router = None

pared_dc = {}

def value_str(v):
    #if inspect.isfunction(v):
    #global used_module
    #if isinstance(v,str):
        #return '"%s"'%v
    #else:
        #used_module.append(value_mod(v))
    module = inspect.getmodule(v)
    return '%s.%s'%(module.__name__,v.__qualname__)

def director_name_to_module_name(director_name):
    if director_name not in pared_dc:
        obj = director.get(director_name) or director_views.get(director_name)
        obj_str = value_str(obj)
        pared_dc[director_name] = obj_str
    else:
        obj_str = pared_dc[director_name]
    return obj_str

def all_name(director_name,kws):
    out =[]
    out.append(director_name_to_module_name(director_name))
    
    if kws.get('director_name'):
        out.append(director_name_to_module_name(kws.get('director_name')))
    if kws.get('_director_name'):
        out.append(director_name_to_module_name(kws.get('_director_name')))   
    if kws.get('row') and kws.get('row').get('_director_name'):
        out.append(director_name_to_module_name( kws.get('row').get('_director_name')   ))   
    return out

def director_transaction_db(director_name,kws):
    """根据director_name返回需要事物的数据库"""
    if router:
        out = []
        paths = all_name(director_name, kws)
        for path in paths:
            out.extend(router.db_for_transaction(path) )
        return list(set(out))
    else:
        return ['default']
   
