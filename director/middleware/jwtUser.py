from threading import currentThread
#from django.core.cache.backends.locmem import LocMemCache
import json
from django.utils.deprecation import MiddlewareMixin
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
import jwt
from django.conf import settings
from helpers.func.dot_dict import read_dict_path
from django.contrib.auth.models import User
from django.contrib import auth

class JwtUser(MiddlewareMixin):

    def process_request(self, request):
        encoded_jwt = request.GET.get('jwt')
        algorithms = read_dict_path(settings,'JWT_USER.algorithms',["HS256"])
        secret  = read_dict_path(settings,'JWT_USER.secret')
        if encoded_jwt:
            jwt_dc = jwt.decode(encoded_jwt, secret, algorithms= algorithms)
            username = jwt_dc.get('user')
            user,created = User.objects.get_or_create(username= username)
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            if created:
                user.is_staff = True
                user.is_valid =  True
                # 新添加的用户,默认分配gourps.id=1的，要保证group.id=1的分组存在
                user.groups.add(1)
                user.save()
            
            auth.login(request,user)         
            
    

        
        
