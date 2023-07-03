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
from .base_data import director,director_views,director_exclude_transaction
from django.db import transaction
from helpers.director.network import argument
from django.conf import settings
import inspect
from helpers.director.exceptions.unauth401 import UnAuth401Exception
from .data_format.json_format import DirectorEncoder
from .exceptions.question import QuestionException
from helpers.func.d_import import import_element
from helpers.func import ex
from .base_data import director_setting,director_view
from .middleware.request_cache import get_request_cache

from .funs.transaction_db import director_transaction_db
import re

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

def tranactionDefault(fun):
    return wrap(fun,'default')

def tranactionDbs(fun,keys):
    def _fun(*args,**kws):
        _fun1 = fun
        for key in keys:
            _fun1 = wrap(_fun1, key)
        return _fun1(*args,**kws)
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
        wraped_ajax_router =  tranactionDefault(ajax_router)
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

@director_view('general/upload')
def _general_upload():
    request = get_request_cache()['request']
    return general_upload(request)


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
    
    # 专门针对modelfield返回详情
    if director_name.startswith('get/'):
        kws = argument.get_argument(request,outtype='dict')
        directorEnt= director.get(director_name)
        rt = directorEnt(**kws,select_for_update=False).get_data_context() 
        dc ={'success':True,'data':rt.get('row')}
        return  HttpResponse(json.dumps(dc,ensure_ascii=False,cls=DirectorEncoder),content_type="application/json")     
    
    if request.method == "GET" or request.META.get('HTTP_REALTYPE')=='json_get':
        return fast_director_view(request, director_name)
    
    # 2021/8/18增加新的逻辑,可以对/dapi/edit/customForm转换为请求d.save_row_for_front,参数是edit/customForm指向的director表单
    kws = argument.get_argument(request,outtype='dict')
    if director_name.startswith('edit/'):
        directorEnt = director_views.get('d.save_row_for_front')
        kws['_director_name'] = director_name#[5:]  
        kws={'row':kws}
    elif director_name.startswith('delete/'):
        directorEnt = director_views.get('d.delete_row')
        kws['_director_name'] = director_name#[6:]
        kws={'row':kws}     
    
    # [1] 使用element来打包 director_view
    elif director_name.startswith('element/'):
        directorEnt = director_views.get('d.director_element_call2')
        rt = re.search('element/(.+)/(\w+)$', director_name)
        director_name = rt.groups()[0]
        attr_name = rt.groups()[1]
        kws['director_name'] = director_name#[6:]
        kws['attr_name'] = attr_name                   
    else:
        directorEnt= director_views.get(director_name)
    if not directorEnt:
        directorEnt = director.get(director_name)
          
    try:
        #kws = argument.get_argument(request,outtype='dict')
        if request.GET.get('transaction') == '0':
            need_transaction = False
        elif director_name in  director_exclude_transaction:
            need_transaction = False
        else:
            need_transaction = True
            
        if inspect.isfunction(directorEnt):
            # 2020/7/6 再次开启 事务
            # 2021/3/7 加入默认事务配置，sportscenter有多个库连接，但是sports库才是主库。原来采用default库，造成重大问题
            if need_transaction:         
                db_names= director_transaction_db(director_name,kws = kws) #  getattr(settings,'REQUEST_TRANSACTION_DB',['default'])
                wraped_directorEnt = tranactionDbs(directorEnt,db_names)
                #wraped_directorEnt = tranactionDefault(directorEnt)
                rt = wraped_directorEnt(**kws)
            else:
                rt = directorEnt(**kws)
                # 2020/3/18 去掉统一的事务，免得造成异步性能不足和死锁
        else:
            # directorEnt is class
            if hasattr(directorEnt,'gen_from_search_args'):
                # 表示是 modeltable子类
                obj = directorEnt.gen_from_search_args(kws)
                real_func = obj.get_data_context
            else:
                obj = directorEnt(**kws)
                real_func = obj.get_context
            #if hasattr(obj,'get_data_context'):
                #real_func = obj.get_data_context
            #else:
                #real_func = obj.get_context
            if need_transaction:
                wraped_directorEnt = tranactionDefault(real_func)
                rt = wraped_directorEnt()
            else:
                rt = real_func()
            #rt = wraped_directorEnt()
            
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
        #dc = {'success':False,'msg':str(e),'data':None,'error':str(e)}
        dc = {'success':False,'msg':str(e),'data':None,}
        rt = HttpResponse(json.dumps(dc,ensure_ascii=False,cls=DirectorEncoder),content_type="application/json") 
    
    except PermissionDenied as e:
        rt = HttpResponse(str(e),status=403)
    if hasattr(request,'on_finally'):
        for callback in request.on_finally:
            callback()
    return rt



@csrf_exempt
def fast_director_view(request,director_name):
    """director_view的快速版本
    
    为了加大并发量，一般只读版本
    """
    kws = argument.get_argument(request,outtype='dict')
    
    if director_name.startswith('element/'):
        directorEnt = director_views.get('d.director_element_call2')
        rt = re.search('element/(.+)/(\w+)$', director_name)
        director_name = rt.groups()[0]
        attr_name = rt.groups()[1]
        kws['director_name'] = director_name#[6:]
        kws['attr_name'] = attr_name           
    else:
        directorEnt= director_views.get(director_name)
    allowed_methods =  ex.read_dict_path(director_setting, '%s.methods'%director_name)
    if allowed_methods and 'GET' not in allowed_methods:
        return HttpResponse('request Method not allowed',status=405)
    if not directorEnt:
        directorEnt = director.get(director_name)
    try:
        # 快速版本里面应该只有fuction,尽量不要使用 modelfields,之类
        if inspect.isfunction(directorEnt):
            rt = directorEnt(**kws)
            
        else:
            # directorEnt is class
            if hasattr(directorEnt,'gen_from_search_args'):
                # 表示是 modeltable子类
                obj = directorEnt.gen_from_search_args(kws)
                real_func = obj.get_data_context
            else:
                obj = directorEnt(**kws)
                real_func = obj.get_context
                
            rt = real_func()

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
        dc = {'success':False,'msg':str(e),'data':None,'error':str(e)}
        rt = HttpResponse(json.dumps(dc,ensure_ascii=False,cls=DirectorEncoder),content_type="application/json") 
        #rt = JsonResponse({'success':False,'msg':str(e)})
    except PermissionDenied as e:
        rt = HttpResponse(str(e),status=403)

    return rt

def helloworld(request):
    return  HttpResponse('hello world')

    

