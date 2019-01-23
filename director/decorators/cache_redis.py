from ..network.myredis import redis_conn
import json

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
            rt = redis_conn.get(cache_name)
            if not rt:
                rt_obj = fun(*args, **kws)
                rt = json.dumps(rt_obj)
                redis_conn.set(cache_name,rt,ex=ex)
            else:
                rt_obj = json.loads(rt)
            return rt_obj
      
        return _fun2
    return _fun