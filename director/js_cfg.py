from helpers.director.base_data import js_tr_list, js_lib_list
from helpers.maintenance.update_static_timestamp import js_stamp_dc,static_url
from django.utils.translation import ugettext as _

def get_tr():
    return {
        '收起':_('收起'),
        "更多":_("更多"),
        "确认":_("确认"),
        "确定":_("确定"),
        "取消":_("取消"),
    }
js_tr_list.append(get_tr)

def get_lib(request): 
    dc = {
        'exfun': static_url( 'js/exfun.pack.js?t=%s&v=6'%js_stamp_dc.get('exfun_pack_js') ),
        'director': static_url( 'js/director.pack.js?t=%s&v=2'%js_stamp_dc.get('director_pack_js') ),
        'moment': '/static/lib/moment2.17.1.min.js',
        'stompjs':'https://cdn.jsdelivr.net/npm/stompjs@2.3.3/lib/stomp.min.js'
        
    }
    if request.META.get('ACCESS_FROM_INTERNET'):
        dc.update({
            'moment':'https://cdn.jsdelivr.net/npm/moment@2.24.0/moment.min.js',
            'moment_zh_cn':'https://cdn.jsdelivr.net/npm/moment@2.24.0/locale/zh-cn.js'
        })

    return dc

js_lib_list.append(get_lib)