from helpers.director.base_data import js_tr_list, js_lib_list
def get_lib(request): 
    dc = {
        #'vuejs': 'https://cdn.bootcss.com/vue/2.5.16/vue.js',
        #'jquery': '/static/lib/jquery3.2.1.min.js',
        #'font_awesome': '/static/lib/font-awesome4.7/font-awesome4.7.min.css',
        #'bootstrap_css': '/static/lib/bootstrap.min.css',
        #'bootstrap': '/static/lib/bootstrap.min.js',
        #'nice_validator': 'https://cdn.bootcss.com/nice-validator/1.1.3/jquery.validator.min.js?local=zh-CN',
        #'nice_validator_css': 'https://cdn.bootcss.com/nice-validator/1.1.3/jquery.validator.min.css',
        
        'exfun': '/static/js/exfun.pack.js',
        'director': '/static/js/director.pack.js',
        
        #'adminlte': 'https://cdn.bootcss.com/admin-lte/2.4.3/js/adminlte.min.js',
        #'adminlte_css': 'https://cdn.bootcss.com/admin-lte/2.4.3/css/AdminLTE.min.css',
        #'adminlte_blue_css': 'https://cdn.bootcss.com/admin-lte/2.4.3/css/skins/skin-blue.min.css',
        
        'nprogress': '/static/lib/nprogress/nprogress.min.js',
        'nprogress_css': '/static/lib/nprogress/nprogress.min.css',
        #'layer': 'https://cdn.bootcss.com/layer/3.1.0/layer.js',
        
        'element': '/static/lib/element/index.js',
        'element_css': '/static/lib/element/index.css',
        'md5_js': '/static/lib/md5.min.js',
    }
    return dc

js_lib_list.append(get_lib)