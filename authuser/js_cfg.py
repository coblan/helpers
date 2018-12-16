from helpers.director.base_data import js_tr_list, js_lib_list
from helpers.maintenance.update_static_timestamp import js_stamp_dc
def get_lib(request): 
    dc = {        
        'authuser': '/static/js/authuser.pack.js?t=%s'%js_stamp_dc.get('authuser_pack_js'),
    }
    return dc

js_lib_list.append(get_lib)