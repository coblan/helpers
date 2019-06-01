from helpers.director.base_data import js_tr_list, js_lib_list
from helpers.maintenance.update_static_timestamp import js_stamp_dc
def get_lib(request): 
    dc = {
        'exfun': '/static/js/exfun.pack.js?t=%s'%js_stamp_dc.get('exfun_pack_js'),
        'director': '/static/js/director.pack.js?t=%s&v=2'%js_stamp_dc.get('director_pack_js'),
        'moment': '/static/lib/moment2.17.1.min.js',
        
    }
    if request.META.get('ACCESS_FROM_INTERNET'):
        dc.update({
            'moment':'https://cdn.jsdelivr.net/npm/moment@2.24.0/moment.min.js'
        })

    return dc

js_lib_list.append(get_lib)