from threading import currentThread
#from django.core.cache.backends.locmem import LocMemCache
import json
from django.utils.deprecation import MiddlewareMixin
from functools import wraps

# 每个request请求的全局对象
_request_cache = {
    'named_ctx':{}
}
_installed_middleware = False

#class NoUser(object):
    #def __init__(self, *args, **kwargs):
        #self.username='systemcall'
        #self.is_authenticated = False

class NoRequest(object):
    def __init__(self, *args, **kwargs):
        from django.contrib.auth.models import AnonymousUser
        self.user = AnonymousUser()

def get_request_cache():
    if _installed_middleware:
        assert _installed_middleware, 'GlobalCacheMiddleware not loaded'
        request_cache=  _request_cache.get( currentThread() )
        if request_cache:
            return request_cache
    no_request =NoRequest()
    return {
        'request':no_request,
        'named_ctx':{},
    }

def request_cache(fun): 
    @wraps(fun)
    def _fun(*args, **kws):
        cache = get_request_cache()
        if kws.get('cache_key'):
            key = kws.get('cache_key')
        else:
            key = str( hash(fun))
            if args:
                for item in args:
                    key += '%s_%s'%(item.__class__.__name__, id(item) )
            if kws:
                key += str( hash(json.dumps(kws, sort_keys=True)) )
            
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
            'named_ctx':{},
            'response_cache':{}
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