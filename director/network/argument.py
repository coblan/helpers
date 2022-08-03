# encoding:utf-8

from __future__ import unicode_literals
from __future__ import absolute_import

from urllib import parse
from ..data_format.dot_dict import DotObj
import re
import json
import hashlib
from django.conf import settings
import inspect
import time

def get_argument(request,outtype='obj'):
    """
    """
    
    if request.method=='POST':
        if request.body and request.body.strip().decode('utf-8').startswith(('{','[')):
            try:
                dc=json.loads(request.body.decode('utf-8'))
            except Exception as e:
                raise UserWarning(str(e) )
        else:
            dc = request.POST.dict()
        #else:
            #dc =parse.parse_qs(request.body)
            
            #for k,v in dc.items():
                #if isinstance(v,list):
                    #dc[k]=v[0]
    else:
        dc =  request.GET.dict()
    if outtype=='dict':
        return dc
    else:
        return DotObj( dc )
    
def validate_argument(dc,validate_dict={},eliminate = False):
    """
    验证@dc 满足validate_dict 的需求
    
     argument.validate_argument(row,{
                'InvoiceNum':[argument.int_str],
            })
    """
    if isinstance(dc,DotObj):
        dc=dc.__dict__
    org_dc = dict(dc)
    for k,v in validate_dict.items():
        value = dc.get(k)
        for validator in v:
            if validator == null_break:
                if(null_break(value, k)):
                    break
                else:
                    continue
            
            if 'params' in inspect.getargspec(validator).args:
                value = validator(value,k,params=org_dc)
            else:
                value=validator(value,k)
        # 确保不会给 dc 增加 值为none的字段
        if value ==None:
            if k in dc:
                dc[k] = None
        else:
            dc[k]=value
    if eliminate:
        for k in dict(dc):
            if k not in validate_dict:
                dc.pop(k)
    return DotObj( dc )

def dict2url(dc:dict) -> str:
    outls =[]
    for k,v in dc.items():
        outls.append('%s=%s'%(k,v) )  
    return '&'.join(outls)

def url2dict(url:str) -> dict:
    return dict(parse.parse_qsl(parse.urlsplit(url).query))

def sign_args(kws,secret):
    "排序参数，并且签名"
    sign_str = ''
    for k,v in sorted(kws.items(),key=lambda p:p[0]):
        if v:
            sign_str += '{key}={value}&'.format(key=k,value=v)
    sign_str = sign_str + 'secret=' + secret
    return hashlib.md5(sign_str.encode('utf-8')).hexdigest().upper()   



def null_break(value,name):
    "如果是None值，就退出验证栈"
    if value is None or (isinstance(value,str) and value.strip() ==''):
        return True
    else:
        return False
    
def not_null(value,name):
    
    if value is None or (isinstance(value,str) and value.strip() ==''):
        raise UserWarning('%s should not be null'%name)
    return value


def model_instance(model,field='pk'):
    "判断value是否是model instance(默认使用pk值查询)"
    def _model_validator(value,name):
        try:
            if value:
                dc={field:value}
                return model.objects.get(**dc)
        except model.DoesNotExist as e:
            raise UserWarning('%(name)s=%(value)s can not be find'%{'name':name,'value':value})
    return _model_validator

def model_instance_list(model,field='pk'):
    "判断value是否是model instance(默认使用pk值查询)"
    def _model_validator(value,name):
        try:
            if value:
                dc ={'%s__in'%field:value}
                inst_dc = {}
                for inst in model.objects.filter(**dc):
                    inst_dc[ str( getattr(inst,field) )] = inst
                out_ls = []
                for ii in value:
                    if str(ii ) in inst_dc:
                        out_ls.append( inst_dc[str(ii )] )
                    else:
                        raise UserWarning('%s=%s can not be find'%(field,ii))
                return out_ls
                    
        except model.DoesNotExist as e:
            raise UserWarning('%(name)s=%(value)s can not be find'%{'name':name,'value':value})
    return _model_validator

"""
ls={
    'zk':[not_null,model_instance(model)],
    'chepai':[model_instance(model)]
}
"""

def sign(src_field:list,secret=settings.SECRET_KEY):
    def _fun(value,name,params):
        dc ={}
        for i in src_field:
            dc[i] = params[i]
        if sign_args(dc, secret) != value:
            raise UserWarning('sign not valid')
    return _fun

def timestamp_span(span):
    def _fun(value,name):
        fvalue = float(value)
        if time.time() - fvalue > span:
            raise UserWarning('%s has expired'%name)
    return _fun

def default(def_value):
    "设置默认值,与not_null 相互排斥"
    def _default(value,name):
        adpt_value = value
        if isinstance(value,str):
            adpt_value = value.strip()        
        if value is None or adpt_value =='':
            return def_value
        else:
            return value
    return _default

def remove_dot(value,name):
    " 1,234.00 转换为  1234.00"
    if isinstance(value,str):
        return value.replace(',','')
    else:
        return value
        
def dot_list_str(value,name):
    if not value:
        return ''
    else:
        return ','.join(value)

def is_list(value,name):
    "value是否为list"
    if not value:
        return []
    if not isinstance(value,(list,tuple)):
        raise UserWarning('%s 需要传入列表数据'%name)
    else:
        return value

def list_unique(value,name):
    tmp =[]
    for inst in value:
        if inst in tmp:
            raise UserWarning('%s不能重复'%name)
        else:
            tmp.append(inst)
    return value

def list_unique_pass_none(value,name):
    "不检查None形的重复"
    tmp =[]
    for inst in value:
        if inst in tmp:
            raise UserWarning('%s不能重复'%name)
        elif inst:
            tmp.append(inst)
    return value

def failmsg(fun,msg):
    "定制自定义的消息"
    def _fun(value,name):
        try :
            return fun(value,name)
        except UserWarning as e:
            raise UserWarning(msg)
    return _fun

def int_str(value,name):
    """确保可以 转换为int"""
    if value:
        try:
            return int(value)
        except ValueError as e:
            raise UserWarning('%(name)s=%(value)s 不能转换为 int'%{'name':name,'value':value})
    else:
        return value

def float_str(value,name):
    try:
        return float(value)
    except ValueError:
        raise UserWarning('%s不能转换为数字(包含小数)'%name)
    #try:
        #if value is not None:
            #return int(value)
    #except ValueError as e:
        #raise UserWarning('%(name)s=%(value)s could not be covert to int'%{'name':name,'value':value})

def choice_in(choices):
    def _choice_in(value,name):
        if value and value not in choices:
            raise UserWarning('%(name)s=%(value)s can not be find in %(choices)s'%{'name':name,'value':value,'choices':choices})
        else:
            return value
    return _choice_in

def datetime(value,name):
    try:
        if value:
            return value.strptime('%Y-%m-%d %H:%M:%S')
        else:
            return ''
    except :
        raise UserWarning('%(name)s could not be convert to datetime')
        