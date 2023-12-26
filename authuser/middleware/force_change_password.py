from django.contrib.sessions.models import Session

from django.http import HttpResponseRedirect
from .. models import PasswordInfo

class ForceChangePasswordMiddleware:
    # Called only once when the web server starts
    def __init__(self, get_response):
        self.get_response = get_response

    # Called once per request
    def __call__(self, request):
        # This codition is required because anonymous users 
        # dont have access to 'logged_in_user'
        if request.user.is_authenticated:
            if request.COOKIES.get('need_change_password'):
                HttpResponseRedirect('/accounts/pswd')
        response = self.get_response(request)
        return response
    


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