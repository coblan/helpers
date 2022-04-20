from helpers.director.base_data import js_tr_list, js_lib_list
from django.utils.translation import ugettext as _
from helpers.maintenance.short_cut import js_stamp_dc,static_url

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
        'mobile': static_url( 'js/mobile.pack.js?t=%s&v=16'%js_stamp_dc.get('mobile_pack_js') ), 
        'mobile2': static_url( 'js/mobile2.pack.js?t=%s&v=16'%js_stamp_dc.get('mobile2_pack_js') ), 
        'mint_ui':'https://cdn.jsdelivr.net/npm/mint-ui@2.2.13/lib/index.js',
        'mint_ui_css':'https://cdn.jsdelivr.net/npm/mint-ui@2.2.13/lib/style.min.css',
        #'vant':'https://cdn.jsdelivr.net/npm/vant@1.6/lib/vant.min.js',
        #'vant_css':'https://cdn.jsdelivr.net/npm/vant@1.6/lib/index.css',
        #'vant':'https://cdn.jsdelivr.net/npm/vant@2.6/lib/vant.min.js',
        #'vant_css':'https://cdn.jsdelivr.net/npm/vant@2.6/lib/index.css',
        'vant':'https://cdn.jsdelivr.net/npm/vant@2.12.6/lib/vant.min.js',
        'vant_css':'https://cdn.jsdelivr.net/npm/vant@2.12.6/lib/index.css',
        'cube_ui':'https://cdn.jsdelivr.net/npm/cube-ui@1.12.14/lib/index.min.js',
        'cube_ui_css':'https://cdn.jsdelivr.net/npm/cube-ui@1.12.14/lib/cube.min.css',
        'velocity':'https://cdn.jsdelivr.net/npm/velocity-animate@1.5.2/velocity.min.js'
    }
    return dc

js_lib_list.append(get_lib)