# encoding:utf-8

import os
from django.conf import settings
from helpers.func.dot_dict import DotObj
import urllib

def get_static_obj(path):
    if not os.path.exists(path):
        dc= {}
    else:
        dc={}
        for name in os.listdir(path):
            abs_path=os.path.join(path,name)
            if os.path.isfile(abs_path):
                key=name.replace('.','_')
                dc[key]=int(os.path.getmtime(abs_path))
    
    return DotObj(dc)

def get_static_dc(path):
    if not os.path.exists(path):
        return {}
    
    dc={}
    for name in os.listdir(path):
        abs_path=os.path.join(path,name)
        if os.path.isfile(abs_path):
            key=name.replace('.','_')
            dc[key]=int(os.path.getmtime(abs_path))
    
    return dc

def static_url(path):
    return urllib.parse.urljoin(settings.STATIC_URL,path)

org_static_file_path=os.path.join(settings.BASE_DIR,'static')
volatile_static_file_path=os.path.join(org_static_file_path,'js')

# 这个名字太长了
static_file_timestamp_dict=get_static_obj(volatile_static_file_path)

# 下面这个名字短点
js_stamp=get_static_obj(volatile_static_file_path)

js_stamp_dc = get_static_dc(volatile_static_file_path)



