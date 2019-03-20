import time
from helpers.director.kv import get_value,set_value,clear_value,lock_created
def single_call_in_db(fun): 
    """
    
    """
    def _fun2(*args,**kws): 
        key = '%s.%s'%(fun.__module__ ,fun.__name__) #str( hash(fun))
        if args:
            for item in args:
                key += '%s_%s'%(item.__class__.__name__, id(item) )
        if kws:
            key += str( hash(json.dumps(kws, sort_keys=True)) )
            
        cache_name = 'lock:fun:%s'%key
        
        created = lock_created(cache_name,1)
        if created:
            rt_obj = fun(*args, **kws)
            clear_value(cache_name)
        else:
            count =0
            while(True):
                count+=200
                time.sleep(200)
                if not get_value(cache_name):
                    break
                if count>10000:
                    raise UserWarning('等待同步函数请求超时')
            rt_obj = fun(*args, **kws)
        return rt_obj
  
    return _fun2

one_call_at_same_time = single_call_in_db