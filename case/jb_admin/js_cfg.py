from helpers.director.base_data import js_tr_list, js_lib_list
from django.utils.translation import ugettext as _
from helpers.maintenance.update_static_timestamp import js_stamp_dc

def get_tr():
    return {
        'base_setting':_('Basic Setting'),
        'language':_('Language'),
        'back':_('back'),
        'search':_('Search'),
        'change_password':_('Change Password'),
        'logout':_('LogOut'),
        'login':_('LogIn'), 
        
    }

js_tr_list.append(get_tr)

def get_lib(request): 
    dc = {
        'vuejs': 'https://cdn.bootcss.com/vue/2.5.16/vue.js',
        'jquery': '/static/lib/jquery3.2.1.min.js',
        'font_awesome': '/static/lib/font-awesome4.7/font-awesome4.7.min.css',
        'bootstrap_css': '/static/lib/bootstrap.min.css',
        'bootstrap': '/static/lib/bootstrap.min.js',
        'nice_validator': 'https://cdn.bootcss.com/nice-validator/1.1.3/jquery.validator.min.js?local=zh-CN',
        'nice_validator_css': 'https://cdn.bootcss.com/nice-validator/1.1.3/jquery.validator.min.css',
        
        #'exfun': '/static/js/exfun.pack.js',
        #'director': '/static/js/director.pack.js',
        
        'adminlte': 'https://cdn.bootcss.com/admin-lte/2.4.3/js/adminlte.min.js',
        'adminlte_css': 'https://cdn.bootcss.com/admin-lte/2.4.3/css/AdminLTE.min.css',
        'adminlte_blue_css': 'https://cdn.bootcss.com/admin-lte/2.4.3/css/skins/skin-blue.min.css',
        
        'nprogress': 'https://cdn.bootcss.com/nprogress/0.2.0/nprogress.min.js',
        'nprogress_css': 'https://cdn.bootcss.com/nprogress/0.2.0/nprogress.min.css',
        'layer': 'https://cdn.bootcss.com/layer/3.1.0/layer.js',
        'layer_css':'https://cdn.bootcss.com/layer/3.1.0/theme/default/layer.css',
        #'element': 'https://unpkg.com/element-ui/lib/index.js',
        #'element_css': 'https://unpkg.com/element-ui/lib/theme-chalk/index.css',
        #'md5': 'https://cdn.bootcss.com/blueimp-md5/2.10.0/js/md5.min.js',
        'jb_admin_pack_js': '/static/js/jb_admin.pack.js?t=%s'%js_stamp_dc.get('jb_admin_pack_js'),
    }
    return dc

js_lib_list.append(get_lib)