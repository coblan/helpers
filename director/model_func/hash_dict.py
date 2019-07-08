# encoding:utf-8
from __future__ import unicode_literals
from hashlib import md5

from base64 import b64encode
import json

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

def mark_dict(dc,keys=None):
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
        out_dc[k] = str(v)
    return out_dc

def dif_mark_dict(dc,mark,keys=None):
    dif_dc = {}
    for k,v in mark.items():
        if keys and k not in keys:
            continue
        if str(dc[k]) != v:
            dif_dc[k] = v
    return dif_dc