from helpers.director.base_data import js_tr_list, js_lib_list
from django.utils.translation import ugettext as _
from helpers.maintenance.update_static_timestamp import js_stamp_dc

def get_tr():
    return {
        #'base_setting':_('Basic Setting'),
        #'language':_('Language'),
        #'back':_('back'),
        #'search': _('Refresh'),
        #'change_password':_('Change Password'),
        #'logout':_('LogOut'),
        #'login':_('LogIn'), 
        
    }

js_tr_list.append(get_tr)

def get_lib(request): 
    dc = {

        'mobile': '/static/js/mobile.pack.js?t=%s&v=1'%js_stamp_dc.get('mobile_pack_js'), 
        'mint_ui':'https://cdn.jsdelivr.net/npm/mint-ui@2.2.13/lib/index.js',
        'mint_ui_css':'https://cdn.jsdelivr.net/npm/mint-ui@2.2.13/lib/style.min.css',
        'vant':'https://cdn.jsdelivr.net/npm/vant@1.6.13/lib/index.min.js',
        'cube_ui':'https://cdn.jsdelivr.net/npm/cube-ui@1.12.14/lib/index.min.js',
        'cube_ui_css':'https://cdn.jsdelivr.net/npm/cube-ui@1.12.14/lib/cube.min.css'
    }
    return dc

js_lib_list.append(get_lib)