# encoding:utf-8

from django.core.exceptions import PermissionDenied
from .model_admin.permit import has_permit

def need_login(fun):
    def _fun(request,*args,**kw):
        if request.user.is_authenticated():
            return fun(request,*args,**kw)
        else:
            raise PermissionDenied('need login ! If you access with session_id,it is mainly because session_id has been destroyed,this is happen when login at same device with diffrent accounts,the older session_id will be destroyed')
    return _fun

def need_permit(fun):
    """还没想好怎么写"""
    def _fun(request,*args,**kw):
        if request.user.is_authenticated():
            return fun(request,*args,**kw)
        else:
            raise PermissionDenied('need login ! If you access with session_id,it is mainly because session_id has been destroyed,this is happen when login at same device with diffrent accounts,the older session_id will be destroyed')
    return _fun