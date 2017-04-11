# encoding:utf-8

from __future__ import unicode_literals
from __future__ import absolute_import

import urlparse

def get_argument(request):
    if request.method=='POST':
        dc =urlparse.parse_qs(request.body)
        for k,v in dc.items():
            if isinstance(v,list):
                dc[k]=v[0]
        return dc
    else:
        return dict(request.GET)

def validate_argument(dc,validate_dict):
    for k,v in validate_dict.items():
        value = dc.get(k)
        for validator in v:
            value=validator(value,k)
        dc[k]=value
    return dc


def not_null(value,name):
    if not value:
        raise UserWarning,'%s should not be null'%name
    return value


def model_instance(model):
    def _model_validator(value,name):
        try:
            value = model.objects.get(pk=value)
        except model.DoesNotExist as e:
            raise UserWarning,'%(name)s=%(value)s can not be find'%{'name':name,'value':value}
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
        

def int_str(value,name):
    try:
        value=int(value)
    except ValueError as e:
        raise UserWarning,'%(name)s=%(value)s counld not be covert to int'%{'name':name,'value':value}
    return value