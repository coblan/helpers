
import json
from helpers.director.kv import get_value,set_value,lock_created,clear_value
import time
from django.conf import settings

import hashlib

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
                m = hashlib.md5()
                kws_str = json.dumps(kws, sort_keys=True)
                m.update(kws_str.encode('utf-8')) #参数必须是byte类型，否则报Unicode-objects must be encoded before hashing错误
                md5value=m.hexdigest()            
                key += '_'+md5value

            cache_name = 'cache:fun:%s'%key
            rt = redis_conn.get(cache_name.encode('utf-8'))
            if not rt:
                lock_key = 'lock:fun:%s'%key
                created = lock_created(lock_key,1)
                if created:
                    rt_obj = fun(*args, **kws)
                    rt = json.dumps(rt_obj)
                    redis_conn.set(cache_name,rt,ex=ex)
                    clear_value(lock_key)
                else:
                    count = 0
                    while(True):
                        if count>10000:
                            raise UserWarning('缓存等待同步函数执行完成超时')
                        count +=200
                        time.sleep(200)
                        if not get_value(lock_key):
                            rt = redis_conn.get(cache_name.encode('utf-8'))
                            rt_obj =json.loads(rt.decode('utf-8'))
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
                m = hashlib.md5()
                kws_str = json.dumps(kws, sort_keys=True)
                m.update(kws_str.encode('utf-8')) #参数必须是byte类型，否则报Unicode-objects must be encoded before hashing错误
                md5value=m.hexdigest()            
                key += '_'+md5value
                
            cache_name = 'cache:fun:%s'%key
            rt = get_value(cache_name)
            expired = False
            if rt:
                dc = json.loads(rt)
                if dc['snapshot'] +dc['ex'] < time.time():
                    expired=True
                    
            if not rt or expired:
                #lock_key = 'lock:fun:%s'%key
             
                    #created = lock_created(lock_key,1)
                    #if created:
                rt_obj = fun(*args, **kws)
                dc = {
                    'value':rt_obj,
                    'ex':ex,
                    'snapshot':time.time()
                }
                set_value(cache_name,json.dumps(dc))  
 
                    #clear_value(lock_key)
                #else:
                    #count = 0
                    #while(True):
                        #if count>10000:
                            #raise UserWarning('缓存等待同步函数执行完成超时')
                        #count +=200
                        #time.sleep(200)
                        #if not get_value(lock_key):
                            #rt = get_value(cache_name)
                            #rt_obj =json.loads(rt)['value']
                        
               
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