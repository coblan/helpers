from threading import currentThread
#from django.core.cache.backends.locmem import LocMemCache
import json
from django.utils.deprecation import MiddlewareMixin

_request_cache = {}
_installed_middleware = False

def get_request_cache():
    assert _installed_middleware, 'GlobalCacheMiddleware not loaded'
    return _request_cache[currentThread()]

def request_cache(fun): 
    def _fun(*args, **kws):
        cache = get_request_cache()
        key = hash(fun)
        if args:
            key += hash(args)
        if kws:
            key += hash(json.dumps(kws, sort_keys=True))
            
        if cache.get(key):
            return cache.get(key)
        else:
            rt = fun(*args, **kws)
            cache[key] = rt
            return rt
    return _fun

# LocMemCache is a threadsafe local memory cache
#class RequestCache(LocMemCache):
    #def __init__(self):
        #name = 'locmemcache@%i' % hash(currentThread())
        #params = dict()
        #super(RequestCache, self).__init__(name, params)

class RequestCacheMiddleware(MiddlewareMixin):
    def __init__(self,*args,**kws):
        global _installed_middleware
        _installed_middleware = True
        super().__init__(*args,**kws)

    def process_request(self, request):
        cache = {
            'request': request,
            'msg': [],
            }  #_request_cache.get(currentThread()) or RequestCache()
        _request_cache[currentThread()] = cache
        
        #cache.clear()
    
    def process_response(self, request, response):
        """
        Delete user info
        """
        if currentThread() in _request_cache:
            _request_cache.pop( currentThread() )

        return response

    def process_exception(self, request, exception):
        """
        Delete user info
        """
        if currentThread() in _request_cache:
            _request_cache.pop( currentThread() )
        
        
"""
MIDDLEWARE_CLASSES = (
    ...
    'myapp.request_cache.RequestCacheMiddleware'
)
You may then use the cache as follows:

from myapp.request_cache import get_request_cache

cache = get_request_cache()

"""