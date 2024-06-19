from helpers.director.base_data import js_tr_list, js_lib_list
from helpers.maintenance.update_static_timestamp import js_stamp_dc
from django.utils.translation import gettext as _
from django.utils.translation import pgettext

def get_tr():
    return {
        "登录":_("登录"),
        "密码":_("密码"),
        "下次自动登录":_("下次自动登录"),
        "用户登录":pgettext("user_login","用户登录"),
        "欢迎登录后台管理系统":_("欢迎登录后台管理系统"),
        '验证码':_('验证码'),
        '请输入验证码':_('请输入验证码'),
        '用户名':pgettext("user_login",'用户名'),
        '请输入用户名':_('请输入用户名'),
        '请输入密码':_('请输入密码')
        
    }


js_tr_list.append(get_tr)

def get_lib(request): 
    dc = {        
        'authuser': '/static/js/authuser.pack.js?t=%s'%js_stamp_dc.get('authuser_pack_js'),
    }
    return dc

js_lib_list.append(get_lib)