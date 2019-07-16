from threading import currentThread
#from django.core.cache.backends.locmem import LocMemCache
import json
from django.utils.deprecation import MiddlewareMixin
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User

class TokenUser(MiddlewareMixin):

    def process_request(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        if not token:
            token=request.GET.get('token')
        if token:
            request.COOKIES['sessionid'] = token
    

        
        
