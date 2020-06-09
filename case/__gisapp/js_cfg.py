from helpers.director.base_data import js_tr_list, js_lib_list
from django.utils.translation import ugettext as _


def get_lib(request): 
    dc = {
        'gaode_css':'http://cache.amap.com/lbs/static/main1119.css',
        'gaode_js': 'http://webapi.amap.com/maps?v=1.4.6&key=您申请的key值',
        #'gaode_js':'http://webapi.amap.com/maps?v=1.3&key=0909294a753dfe00a0aa124b6ecb93eb&plugin=AMap.PolyEditor,AMap.CircleEditor,AMap.MouseTool',
        'gaode_addtoolbar_js':'http://cache.amap.com/lbs/static/addToolbar.js'

    }
    return dc

js_lib_list.append(get_lib)