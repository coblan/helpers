#encoding:utf-8
from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.core.exceptions import PermissionDenied
import json

from pydoc import locate
from django.utils.translation import ugettext as _
from . import ajax
import urllib
from django.apps import apps
#from helpers.func.network.ajax_router import ajax_router
from .network.ajax_router import ajax_router
from .recv_file import GeneralUpload
from django.views.decorators.csrf import csrf_exempt
from .network.ckeditor import Ckeditor
from .base_data import director,director_views
from django.db import transaction
from helpers.director.network import argument
from django.conf import settings
import inspect
from helpers.director.exceptions.unauth401 import UnAuth401Exception
from .data_format.json_format import DirectorEncoder
from .exceptions.question import QuestionException
from helpers.func.d_import import import_element

import logging
req_log = logging.getLogger('general_log')

"""
>5>helpers/port.rst>
总的ajax view
===============
源码路径为:director/views.ajax_views

作用是，将所有模块的ajax访问，聚集到一个url，再根据url中的app路由到不同app.ajax模块去。

该函数的url现在嵌入到了director.urls中，所以url设置为::

    from helpers.director import urls as director_urls
        url(r'^_ajax/(?P<app>\w+)?/?$',director_views.ajax_views,name='ajax_url'),
    url(r'^_ajax/?$',director_views.ajax_views), 
<-<
"""

def wrap(fun,key):
    def _fun(*arg,**kws):
        with transaction.atomic(using= key):
            return fun(*arg,**kws)
    return _fun

def transactionall(fun):
    keys = settings.DATABASES.keys()
    def _fun(*args,**kws):
        _fun1 = fun
        for key in keys:
            _fun1 = wrap(_fun1, key)
        return _fun1(*args,**kws)
    return _fun



@csrf_exempt
def ajax_views(request,app=None):
    if not app:
        ajax_module = ajax
    else:
        conf= apps.get_app_config(app)
        app_dot_path=conf.module.__name__
        ajax_module=locate('%(app)s.ajax'%{'app':app_dot_path})
    try:
        #keys = settings.DATABASES.keys
        
        #def _fun(key,fun,*args,**kws):
            #with transaction.atomic(using=key):
                #fun(*args,**kws)
        #for key in keys:
            #fun = _fun()
        #with transaction.atomic(using=maindb):
        wraped_ajax_router = transactionall(ajax_router)
        rt= wraped_ajax_router(request, ajax_module.get_global())
        #rt = ajax_router(request, ajax_module.get_global())
            
    #except KeyError as e:
        #rt={'success':False,'msg':'key error '+str(e) +' \n may function name error'}
    except UnAuth401Exception as e:
        return HttpResponse(str(e),status=401)
    except UserWarning as e:
        rt = {'success': False, 'msg': str(e)}
    if isinstance(rt, HttpResponse):
        return rt
    else:
        return HttpResponse(json.dumps(rt,ensure_ascii=False,cls=DirectorEncoder),content_type="application/json")  
    
@csrf_exempt
def general_upload(request):
    if request.GET.get('director'):
        UploadView=director.get(request.GET.get('director'))
        return UploadView().asView(request)
    if getattr(settings,'MEDIA_SAVER',None):
        uploader_str = getattr(settings,'MEDIA_SAVER').get('class')
        uploader = import_element(uploader_str)
        return uploader().asView(request)
    else:
        return GeneralUpload().asView(request)

@csrf_exempt
def ckeditor(request): 
    if getattr(settings,'CKEDITOR_SAVER',None):
        uploader_str = getattr(settings,'CKEDITOR_SAVER').get('class')
        uploader = import_element(uploader_str)
        return uploader().RecieveView(request)
    else:
        return Ckeditor().RecieveView(request)


def export_excel(request): 
    director_name = request.GET.get('director_name')
    search_args = dict( request.GET )
    
    table_cls = director.get(director_name)
    table_obj = table_cls.parse_request(request)  #table_cls.gen_from_search_args(search_args,request.user)
    wb = table_obj.get_excel()
    fl_name = director_name.replace('.', '_')
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=%s.xlsx' % fl_name
    wb.save(response)
    return response 

@csrf_exempt
def director_view(request,director_name):
    """将director函数以api的方式直接暴露出去"""
    directorEnt= director_views.get(director_name)
    if not directorEnt:
        directorEnt = director.get(director_name)
    try:
        kws = argument.get_argument(request,outtype='dict')
        if inspect.isfunction(directorEnt):
            # 2020/7/6 再次开启 事务
            #rt = directorEnt(**kws)
            # 2020/3/18 去掉统一的事务，免得造成异步性能不足和死锁
            wraped_directorEnt = transactionall(directorEnt)
            rt = wraped_directorEnt(**kws)
        else:
            # directorEnt is class
            obj = directorEnt(**kws)
            if hasattr(obj,'get_data_context'):
                wraped_directorEnt = transactionall(obj.get_data_context) # obj.get_data_context # 
            else:
                wraped_directorEnt = transactionall(obj.get_context) # obj.get_context # 
            rt = wraped_directorEnt()
        if isinstance(rt,HttpResponse):
            # 直接返回
            pass
        else:
            dc ={'success':True,'data':rt}
            #rt = JsonResponse(dc,safe=False,ensure_ascii=False)
            rt = HttpResponse(json.dumps(dc,ensure_ascii=False,cls=DirectorEncoder),content_type="application/json") 
    except UnAuth401Exception as e:
        return HttpResponse(str(e),status=401)
    except QuestionException as e:
        dc= {'success':True,'_question':str(e)}
        rt = HttpResponse(json.dumps(dc,ensure_ascii=False,cls=DirectorEncoder),content_type="application/json") 
    except UserWarning as e:
        dc = {'success':False,'msg':str(e)}
        rt = HttpResponse(json.dumps(dc,ensure_ascii=False,cls=DirectorEncoder),content_type="application/json") 
        #rt = JsonResponse({'success':False,'msg':str(e)})
    except PermissionDenied as e:
        rt = HttpResponse(str(e),status=403)

    return rt
    

    

