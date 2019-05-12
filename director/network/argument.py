# encoding:utf-8

from __future__ import unicode_literals
from __future__ import absolute_import

from urllib import parse
from ..data_format.dot_dict import DotObj
import re
import json
import hashlib

def get_argument(request,outtype='obj'):
    """
    """
    
    if request.method=='POST':
        if request.body and re.match('{.+}|\[.+\]',request.body.decode('utf-8')):
            dc=json.loads(request.body)
        else:
            dc =parse.parse_qs(request.body)
            
        for k,v in dc.items():
            if isinstance(v,list):
                dc[k]=v[0]
    else:
        dc =  request.GET.dict()
    if outtype=='dict':
        return dc
    else:
        return DotObj( dc )

def dict2url(dc:dict) -> str:
    outls =[]
    for k,v in dc.items():
        outls.append('%s=%s'%(k,v) )  
    return '&'.join(outls)

def url2dict(url:str) -> dict:
    return dict(parse.parse_qsl(parse.urlsplit(url).query))

def sign_args(kws,secret):
    sign_str = ''
    for k,v in sorted(kws.items(),key=lambda p:p[0]):
        if v:
            sign_str += '{key}={value}&'.format(key=k,value=v)
    sign_str = sign_str + 'key=' + secret
    return hashlib.md5(sign_str.encode('utf-8')).hexdigest().upper()   

def validate_argument(dc,validate_dict={},eliminate = False):
    if isinstance(dc,DotObj):
        dc=dc.__dict__
    for k,v in validate_dict.items():
        value = dc.get(k)
        for validator in v:
            value=validator(value,k)
        dc[k]=value
    if eliminate:
        for k in dict(dc):
            if k not in validate_dict:
                dc.pop(k)
    return DotObj( dc )


def not_null(value,name):
    if not value:
        raise UserWarning('%s should not be null'%name)
    return value


def model_instance(model,field='pk'):
    def _model_validator(value,name):
        try:
            if value:
                dc={field:value}
                return model.objects.get(**dc)
        except model.DoesNotExist as e:
            raise UserWarning('%(name)s=%(value)s can not be find'%{'name':name,'value':value})
    return _model_validator

"""
ls={
    'zk':[not_null,model_instance(model)],
    'chepai':[model_instance(model)]
}
"""

def default(def_value):
    def _default(value,name):
        if not value:
            return def_value
        else:
            return value
    return _default
        
def dot_list_str(value,name):
    if not value:
        return ''
    else:
        return ','.join(value)

def is_list(value,name):
    if not value:
        return []
    if not isinstance(value,(list,tuple)):
        raise UserWarning('%s 需要传入列表数据')
    else:
        return value

def int_str(value,name):
    """确保可以 转换为int"""
    try:
        if value is not None:
            return int(value)
    except ValueError as e:
        raise UserWarning('%(name)s=%(value)s could not be covert to int'%{'name':name,'value':value})

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
        