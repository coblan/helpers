
import json
from helpers.director.kv import get_value,set_value
import time
from django.conf import settings


def cache_redis(ex=None): 
    """
    把函数的返回结果缓存在redis中
    """
    def _fun(fun):
        def _fun2(*args,**kws): 
            key = '%s.%s'%(fun.__module__ ,fun.__name__) #str( hash(fun))
            if args:
                for item in args:
                    key += '%s_%s'%(item.__class__.__name__, id(item) )
            if kws:
                key += str( hash(json.dumps(kws, sort_keys=True)) )
                
            cache_name = 'cache:fun:%s'%key
            rt = redis_conn.get(cache_name.encode('utf-8'))
            if not rt:
                rt_obj = fun(*args, **kws)
                rt = json.dumps(rt_obj)
                redis_conn.set(cache_name,rt,ex=ex)
            else:
                rt_obj = json.loads(rt.decode('utf-8'))
            return rt_obj
      
        return _fun2
    return _fun

def cache_in_db(ex=None): 
    """
    把函数的返回结果缓存在redis中
    """
    def _fun(fun):
        def _fun2(*args,**kws): 
            key = '%s.%s'%(fun.__module__ ,fun.__name__) #str( hash(fun))
            if args:
                for item in args:
                    key += '%s_%s'%(item.__class__.__name__, id(item) )
            if kws:
                key += str( hash(json.dumps(kws, sort_keys=True)) )
                
            cache_name = 'cache:fun:%s'%key
            rt = get_value(cache_name)
            expired = False
            if rt:
                dc = json.loads(rt)
                if dc['snapshot'] +dc['ex'] < time.time():
                    expired=True
                    
            if not rt or expired:
                rt_obj = fun(*args, **kws)
                rt = json.dumps(rt_obj)
                dc = {
                    'value':rt,
                    'ex':ex,
                    'snapshot':time.time()
                }
                set_value(cache_name,json.dumps(dc))
            else:
                rt_obj = dc['value']
            return rt_obj
      
        return _fun2
    return _fun


if getattr(settings,'REDIS_HOST',None):
    from ..network.myredis import redis_conn
    cache_fun = cache_redis
else:
    cache_fun = cache_in_db