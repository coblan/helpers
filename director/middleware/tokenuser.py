from threading import currentThread
#from django.core.cache.backends.locmem import LocMemCache
import json
from django.utils.deprecation import MiddlewareMixin
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User

class TokenUser(MiddlewareMixin):

    def process_request(self, request):
        self.token = None
        token = request.META.get('HTTP_AUTHORIZATION')
        if not token:
            token = request.GET.get('_token')
            self.token = token  # 如果是url带的token,大概率是从外部跳转到浏览器的连接，所以后面需要设置cookie,自动登录。
        if token:
            request.COOKIES['sessionid'] = token
        
    
    def process_response(self, request, response):
        """
        set sessionid to token . if in the browser,can continue browse next page with new sessionid
        """
        if self.token:
            response.set_cookie('sessionid',self.token)

        return response
    

        
        
