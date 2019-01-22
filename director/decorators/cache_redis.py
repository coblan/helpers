from ..network.myredis import redis_conn

def cache_redis(name): 
    def _fun(fun): 
        director[name] = fun
        def _fun2(*args, **kargs): 
            return fun(*args, **kargs)
        return _fun2
    return _fun