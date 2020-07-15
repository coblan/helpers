# encoding:utf-8
from __future__ import unicode_literals
from hashlib import md5

from base64 import b64encode
import json
from django.utils import timezone

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
        if isinstance(v,timezone.datetime):
            out_dc[k] = v.strftime('%y-%m-%d %H:%M:%S')
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
        if k in dc and str(dc[k]) != v:
            dif_dc[k] = v
    return dif_dc