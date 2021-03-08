
import json
from helpers.director.kv import get_value,set_value,lock_created,clear_value,get_json,set_json
import time
from django.conf import settings
from ..data_format.json_format import DirectorEncoder
from django.utils import timezone

import hashlib

if getattr(settings,'REDIS_CACHE',None):
    import redis
    dc = settings.REDIS_CACHE
    redis_conn = redis.Redis(host=dc['host'], port=dc['port'], decode_responses=True,db=dc['db'],password=dc['password']) 
else:
    redis_conn = None

def cache_redis(ex=None,cache_key=None): 
    """
    把函数的返回结果缓存在redis中
    """
    def _fun(fun):
        if redis_conn:
            def _fun2(*args,**kws): 
                if not cache_key:
                    key = '%s.%s'%(fun.__module__ ,fun.__name__) 
                    if args:
                        for item in args:
                            key += '%s_%s'%(item.__class__.__name__, id(item) )
                    if kws:
                        m = hashlib.md5()
                        kws_str = json.dumps(kws, sort_keys=True)
                        m.update(kws_str.encode('utf-8')) #参数必须是byte类型，否则报Unicode-objects must be encoded before hashing错误
                        md5value=m.hexdigest()            
                        key += '_'+md5value
        
                    cache_name = 'cache:fun:%s'%key
                else:
                    cache_name = cache_key
                rt = redis_conn.get(cache_name)
                if not rt:
                    #lock_key = 'lock:fun:%s'%key
                    #created = lock_created(lock_key,1)
                    #if created:
                    rt_obj = fun(*args, **kws)
                    rt = json.dumps(rt_obj,ensure_ascii=False)
                    redis_conn.set(cache_name,rt,ex=ex)
                    #clear_value(lock_key)
                    #else:
                        #count = 0
                        #while(True):
                            #if count>10000:
                                #raise UserWarning('缓存等待同步函数执行完成超时')
                            #count +=200
                            #time.sleep(200)
                            #if not get_value(lock_key):
                                #rt = redis_conn.get(cache_name.encode('utf-8'))
                                #rt_obj =json.loads(rt.decode('utf-8'))
                else:
                    rt_obj = json.loads(rt)
                return rt_obj
            return _fun2
        else:
            return fun
    return _fun

def cache_in_db(ex=None,cache_key=None): 
    """
    把函数的返回结果缓存在redis中
    """
    def _fun(fun):
        def _fun2(*args,**kws): 
            if cache_key is None:
                key = '%s.%s'%(fun.__module__ ,fun.__name__) #str( hash(fun))
                args_str = ''
                if args:
                    args_str += json.dumps(args,cls = DirectorEncoder)
                if kws:
                    args_str += json.dumps(kws,sort_keys=True,cls = DirectorEncoder)
                if args_str:
                    m = hashlib.md5()
                    m.update(args_str.encode('utf-8')) #参数必须是byte类型，否则报Unicode-objects must be encoded before hashing错误
                    md5value=m.hexdigest()            
                    key += '_'+md5value
                cache_name = 'cache:fun:%s'%key
            else:
                cache_name = cache_key
            
            if ex: 
                rt = get_json(cache_name,gte=timezone.now() - timezone.timedelta(seconds=ex))
            else:
                rt = get_json(cache_name)
            
            if rt:
                return rt
            else:
                rt_obj = fun(*args, **kws)
                set_json(cache_name,rt_obj)
                return rt_obj
      
        return _fun2
    return _fun

if getattr(settings,'REDIS_HOST',None):
    from ..network.myredis import redis_conn
    cache_fun = cache_redis
else:
    cache_fun = cache_in_db
    
def clear_fun_cache(key):
    if getattr(settings,'REDIS_HOST',None):
        redis_conn.delete(key)
    else:
        clear_value(key)  # in kv model

