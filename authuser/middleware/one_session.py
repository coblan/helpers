# Remember to add it in the MIDDLEWARE array in the settings.py file
# like so: 'your_app_name.middleware.OneSessionPerUserMiddleware'

'''
参考网址:https://gist.github.com/fleepgeek/92b01d3187cf92b4495d71c69ee818df
参考网址2:https://stackoverflow.com/questions/50833980/how-to-prevent-multiple-login-in-django
'''

from django.contrib.sessions.models import Session
from .. models import LoggedInUser
class OneSessionPerUserMiddleware:
    # Called only once when the web server starts
    def __init__(self, get_response):
        self.get_response = get_response

    # Called once per request
    def __call__(self, request):
        # This codition is required because anonymous users 
        # dont have access to 'logged_in_user'
        if request.user.is_authenticated:
            
            if not getattr(request.user,'logged_in_user',None):
                # 如果遇到老的账号没有启用onesesion情况下登录的
                LoggedInUser.objects.create(user=request.user)
                request.user.refresh_from_db()
            # Gets the user's session_key from the database
            current_session_key =  request.user.logged_in_user.session_key
            # If the session_key exists in the db and it is different from the browser's session
            if current_session_key and current_session_key != request.session.session_key:
                Session.objects.get(session_key=current_session_key).delete()
            # Update the user's session_key in the db
            request.user.logged_in_user.session_key = request.session.session_key
            request.user.logged_in_user.save()

        response = self.get_response(request)
        return response
    


# 下面这部分本来应该放到db_signal.py里面，考虑到按需加载，先放在这里。
# 必须要创建LoggedInUser数据，才能保证OneSessionPerUserMiddleware中间件功能。
from django.contrib.auth import user_logged_in, user_logged_out
from django.dispatch import receiver
#from .models import LoggedInUser

@receiver(user_logged_in)
def on_user_logged_in(sender, request, **kwargs):
    LoggedInUser.objects.get_or_create(user=kwargs.get('user')) 


@receiver(user_logged_out)
def on_user_logged_out(sender, **kwargs):
    LoggedInUser.objects.filter(user=kwargs.get('user')).delete()