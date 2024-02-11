from django.contrib.sessions.models import Session

from django.http import HttpResponseRedirect
from .. models import PasswordInfo
from django.utils import timezone
from helpers.director.shortcut import get_request_cache
from django.utils.deprecation import MiddlewareMixin

class ForceChangePasswordMiddleware(MiddlewareMixin):

    def process_request(self, request):
        pass
        
    
    def process_response(self, request, response):
        """
        """
        if request.path =='/accounts/pswd' : # or request.path.startswith('/dapi'): 
            return response
        
        if request.user.is_authenticated:
            response_cache = get_request_cache()['response_cache']
            if response_cache.get('clear_password_expire'):
                response.delete_cookie('clear_password_expire')
                response.delete_cookie('password_expire')            
            elif response_cache.get('password_expire') ==1:
                """
                第一次 password_expire==1 不能直接跳转，因为api调用跳转了会出问题。
                要等下次请求页面的时候才能跳转。
                """
                response.set_cookie('password_expire',1)
            else:
                if not request.path.startswith('/dapi') and \
                    request.COOKIES.get('password_expire')=='1':
                    response = HttpResponseRedirect('/accounts/pswd')
        return response
    
    
#class ForceChangePasswordMiddleware:
    ## Called only once when the web server starts
    #def __init__(self, get_response):
        #self.get_response = get_response

    ## Called once per request
    #def __call__(self, request):
        ## This codition is required because anonymous users 
        ## dont have access to 'logged_in_user'
        
        #if request.path =='/accounts/pswd' or request.path.startswith('/dapi'): 
            #response = self.get_response(request)
            #return response
        
        #if request.user.is_authenticated:
            ##now = timezone.now()
            ##if not request.COOKIES.get('password_last_change'):
                ##inst,create = PasswordInfo.objects.get_or_create(user = request.user,)
                ##if create:
                    ##inst.last_change = now
                    ##inst.save()
                ##password_last_change= inst.last_change
                ##password_last_change_str = inst.last_change.strftime('%Y-%m-%d %H:%M:%S')
            ##else :
                ##password_last_change_str = request.COOKIES.get('password_last_change')
                ##password_last_change = timezone.datetime.strptime( password_last_change_str,'%Y-%m-%d %H:%M:%S' )
            
            ## 密码要求30天改一次
            ##if password_last_change < now -  timezone.timedelta(days=30): # timezone.timedelta(minutes=5): #
                ##response = HttpResponseRedirect('/accounts/pswd')
                ##response.delete_cookie('password_last_change')
            ##else:
                ##response = self.get_response(request)
                ##response.set_cookie('password_last_change',password_last_change_str)
            #response_cache = get_request_cache()['response_cache']
            #if response_cache.get('clear_password_expire'):
                #response.delete_cookie('clear_password_expire')
                #response.delete_cookie('password_expire')            
            #elif response_cache.get('password_expire'):
                #response = HttpResponseRedirect('/accounts/pswd')
            #else:
                #response = self.get_response(request)
            
        #else:
            #response = self.get_response(request)
        #return response
    


# 下面这部分本来应该放到db_signal.py里面，考虑到按需加载，先放在这里。
# 必须要创建LoggedInUser数据，才能保证OneSessionPerUserMiddleware中间件功能。
#from django.contrib.auth import user_logged_in, user_logged_out
#from django.dispatch import receiver
##from .models import LoggedInUser

#@receiver(user_logged_in)
#def on_user_logged_in(sender, request, **kwargs):
    #LoggedInUser.objects.get_or_create(user=kwargs.get('user')) 


#@receiver(user_logged_out)
#def on_user_logged_out(sender, **kwargs):
    #LoggedInUser.objects.filter(user=kwargs.get('user')).delete()