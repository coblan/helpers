# encoding:utf-8
from __future__ import unicode_literals

from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
import json
from django.core.exceptions import ObjectDoesNotExist
from .middleware.request_cache import get_request_cache

def need_login(fun):
    def _fun(*args,**kw):
        request = get_request_cache().get('request')
        if request.user.is_authenticated():
            return fun(*args,**kw)
        else:
            raise PermissionDenied('Need login !')
    return _fun

def need_permit(fun):
    """还没想好怎么写,暂时没用"""
    def _fun(request,*args,**kw):
        if request.user.is_authenticated():
            return fun(request,*args,**kw)
        else:
            raise PermissionDenied('need login ! If you access with session_id,it is mainly because session_id has been destroyed,this is happen when login at same device with diffrent accounts,the older session_id will be destroyed')
    return _fun

def warn_free(fun):
    def _fun(request,*args,**kw):
        try:
            dc= fun(request,*args,**kw)
        except (UserWarning,ObjectDoesNotExist) as e:
            dc= {
                'status':'fail',
                'msg':str(e)
            }
        if isinstance(dc,HttpResponse):
            return dc
        else:
            return HttpResponse(json.dumps(dc),content_type="application/json")
    return _fun