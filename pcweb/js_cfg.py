from helpers.director.base_data import  js_lib_list
from django.utils.translation import ugettext as _
from helpers.maintenance.short_cut import js_stamp_dc,static_url

def get_lib(request): 
    dc = {
        'pcweb': static_url( 'js/pcweb.pack.js?t=%s&v=1'%js_stamp_dc.get('pcweb_pack_js') ), 
    }
    return dc

js_lib_list.append(get_lib)