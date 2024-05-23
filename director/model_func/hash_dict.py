# encoding:utf-8
from __future__ import unicode_literals
from hashlib import md5

from base64 import b64encode
import json
from django.utils import timezone
import datetime

def hash_dict(dc,keys=None):
    ls =[]
    for k,v in dc.items():
        if keys:
            if k not in keys:
                continue
        if k.startswith('_') or k.startswith('meta_'):
            continue
        if v is True:
            v= 'true'
        if v is False:
            v='false'
        if v is None:
            v='null'
        ls.append("%s:%s"%(k,v))
    ls = sorted(ls)
    code= ';'.join(ls)
    return md5(code.encode('utf-8')).hexdigest() 

def make_mark_dict(dc,keys=None):
    """
    将row生成可以比对的dict，用于overtime比对。要比对的两个row，都要经过这个函数处理一下，才能进行比对。
    1.去除 下划线，meta开始的字段
    2.将none规则化为'' 空字符串，便于比较
    """
    out_dc = {}
    for k,v in dc.items():
        if keys:
            if k not in keys:
                continue
        if k.startswith('_') or k.startswith('meta_'):
            continue
        #if v is True:
            #v= 'true'
        #if v is False:
            #v='false'
        #if v is None:
            #v='null'
        if isinstance(v,(timezone.datetime,datetime.datetime)):
            out_dc[k] = v.strftime('%Y-%m-%d %H:%M:%S')
        elif v is None:
            out_dc[k] = ''
        else:
            out_dc[k] = str(v)
    return out_dc

def dif_mark_dict(dc,mark,include=None,exclude=[]):
    dif_dc = {}
    for k,v in mark.items():
        if include is not None \
           and k not in include:
            continue
        if k in exclude:
            continue
        
        if k in dc and adapt_type(dc[k]) != adapt_type(v):
            dif_dc[k] = adapt_type(v)
    return dif_dc

def adapt_type(v):
    """
    主要目标是用来对比ORM的两个字段的值是否相等[判断 meta_org_dict 是否变化的时候用到]。现在简单粗暴，全部转换为字符串来比较。
    """
    if isinstance(v,(datetime.datetime,timezone.datetime)):
        return v.strftime('%Y-%m-%d %H:%M:%S')
    else:
        return str(v)