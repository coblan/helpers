from helpers.director.base_data import js_tr_list, js_lib_list
from helpers.maintenance.update_static_timestamp import js_stamp_dc
def get_lib(request): 
    dc = {

        #'font_awesome': '/static/lib/font-awesome4.7/font-awesome4.7.min.css',
        #'bootstrap_css': '/static/lib/bootstrap.min.css',
        #'bootstrap': '/static/lib/bootstrap.min.js',
        #'nice_validator': 'https://cdn.bootcss.com/nice-validator/1.1.3/jquery.validator.min.js?local=zh-CN',
        #'nice_validator_css': 'https://cdn.bootcss.com/nice-validator/1.1.3/jquery.validator.min.css',
        
        'exfun': '/static/js/exfun.pack.js?t=%s'%js_stamp_dc.get('exfun_pack_js'),
        'director': '/static/js/director.pack.js?t=%s'%js_stamp_dc.get('director_pack_js'),
        
        #'adminlte': 'https://cdn.bootcss.com/admin-lte/2.4.3/js/adminlte.min.js',
        #'adminlte_css': 'https://cdn.bootcss.com/admin-lte/2.4.3/css/AdminLTE.min.css',
        #'adminlte_blue_css': 'https://cdn.bootcss.com/admin-lte/2.4.3/css/skins/skin-blue.min.css',
        'ckeditor': '/static/lib/ckeditor_4.10.1/ckeditor/ckeditor.js', 
        'nprogress': '/static/lib/nprogress/nprogress.min.js',
        'nprogress_css': '/static/lib/nprogress/nprogress.min.css',
        #'layer': 'https://cdn.bootcss.com/layer/3.1.0/layer.js',
        
        'element': '/static/lib/element/index.js',
        'element_css': '/static/lib/element/index.css',
        'md5_js': '/static/lib/md5.min.js',
        'moment': '/static/lib/moment2.17.1.min.js',
    }
    return dc

js_lib_list.append(get_lib)