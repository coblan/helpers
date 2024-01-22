# 接收事件
from helpers.director.shortcut import get_request_cache
from django.utils import timezone

from helpers.func.sim_signal import sim_signal
from django.http import HttpResponseRedirect
from django.conf import settings
from helpers.func.dot_dict import read_dict_path

@sim_signal.recieve('authuser.login')
def user_login(username=None):
    """
    """
    password_live_seconds = read_dict_path(settings,'AUTHUSER.password_live_seconds',None)
    password_first_change = read_dict_path(settings,'AUTHUSER.password_first_change',None)
    response_cache =  get_request_cache()['response_cache']
    if password_live_seconds or password_first_change:
        """
        如果发现密码过期了,只需要设置cookies。强制反向跳转在中间件中去完成。
        """
        from . models import PasswordInfo
        
        request = get_request_cache()['request']
        if request.user.is_authenticated:
            now = timezone.now()
            inst,create = PasswordInfo.objects.get_or_create(user = request.user,)
            if not inst.last_change:
                inst.last_change = now
                inst.save()
                
                # 首次登录需要修改密码
                if password_first_change:
                    response_cache['password_expire'] =1
            # 密码要求 {password_live_days} 天改一次
            if inst.last_change < now -  timezone.timedelta(seconds=password_live_seconds ): # timezone.timedelta(minutes=5): #
                response_cache['password_expire'] =1

@sim_signal.recieve('authuser.change_password')
def user_change_password(username=None):
    password_live_seconds = read_dict_path(settings,'AUTHUSER.password_live_seconds',None)
    password_first_change = read_dict_path(settings,'AUTHUSER.password_first_change',None)
    response_cache =  get_request_cache()['response_cache']    
    if  password_live_seconds or password_first_change:   
        response_cache.update({
            'clear_password_expire':1
        })    