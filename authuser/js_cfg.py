from helpers.director.base_data import js_tr_list, js_lib_list
from helpers.maintenance.update_static_timestamp import js_stamp_dc
from django.utils.translation import gettext as _

def get_tr():
    return {
        "登录":_("登录"),
        "密码":_("密码"),
        "下次自动登录":_("下次自动登录")
    }

js_tr_list.append(get_tr)

def get_lib(request): 
    dc = {        
        'authuser': '/static/js/authuser.pack.js?t=%s'%js_stamp_dc.get('authuser_pack_js'),
    }
    return dc

js_lib_list.append(get_lib)