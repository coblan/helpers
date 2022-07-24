from helpers.director.base_data import js_tr_list, js_lib_list
from django.utils.translation import ugettext as _
from helpers.maintenance.update_static_timestamp import js_stamp_dc,static_url
from django.conf import settings
def get_tr():
    return {
        'base_setting':_('Basic Setting'),
        'language':_('Language'),
        'back':_('back'),
        'search': _('Refresh'),
        'change_password':_('Change Password'),
        'logout':_('LogOut'),
        'login':_('LogIn'), 
        'element_translation_js':_('element_translation_js'),
        '开始时间':_("开始时间"),
        '结束时间':_("结束时间"),
        "请选择":_("请选择")
    }

js_tr_list.append(get_tr)

def get_lib(request): 
    jsdeliver_crack = True
    
    if settings.DEBUG:
        vue= static_url('lib/vue2.6/vue.js')
    else:
        vue = static_url ( 'lib/vue2.6/vue.min.js' )
        
    dc = {
        'jquery': static_url( 'lib/jquery3.2.1.min.js'),
        'vuejs': vue,
        'vuex': static_url( 'lib/vuex.min.js'), 

        'font_awesome': '/static/lib/font-awesome4.7/font-awesome4.7.min.css',
        'bootstrap_css': '/static/lib/bootstrap.min.css',
        'bootstrap': '/static/lib/bootstrap.min.js',

        'layer': '/static/lib/layer/layer.js',
        'layer_css':'/static/lib/layer/theme/default/layer.css', 
        
        'nice_validator': '/static/lib/nice-validator1.14/dist/jquery.validator.min.js?local=zh-CN',
        'nice_validator_css': '/static/lib/nice-validator1.14/dist/jquery.validator.css',
        #'nice_validator':'https://cdn.staticfile.org/nice-validator/1.1.4/jquery.validator.min.js?local=zh-CN', 
        #'nice_validator_css': 'https://cdn.staticfile.org/nice-validator/1.1.4/jquery.validator.min.css',
        
        #'adminlte': 'https://cdn.staticfile.org/admin-lte/2.4.3/js/adminlte.min.js',
        #'adminlte_css': 'https://cdn.staticfile.org/admin-lte/2.4.3/css/AdminLTE.min.css',
        #'adminlte_blue_css': 'https://cdn.staticfile.org/admin-lte/2.4.3/css/skins/skin-blue.min.css',  
        #'adminlte': '/static/lib/adminlte/dist/js/adminlte.min.js',
        #'adminlte_css': '/static/lib/adminlte/dist/css/AdminLTE.min.css',
        #'adminlte_blue_css': '/static/lib/adminlte/dist/css/skins/skin-blue.min.css',            
        
        'nprogress': '/static/lib/nprogress/nprogress.min.js',
        'nprogress_css': '/static/lib/nprogress/nprogress.min.css',        
        
        
        'element': '/static/lib/element/index.js?v=2.15.7', 
        'element_css':'/static/lib/element/index.css?v=2.15.7', 
        #'element': 'https://cdn.staticfile.org/element-ui/2.4.0/index.js', 
        #'element_css':'https://cdn.staticfile.org/element-ui/2.4.0/theme-chalk/index.css', 
        
        #'md5': 'https://cdn.staticfile.org/blueimp-md5/2.10.0/js/md5.min.js',
         'md5': '/static/lib/md5.min.js',
        
        # 下面是bootcss 的cdn ，但是 不是很稳定
        #'nice_validator': 'https://cdn.bootcss.com/nice-validator/1.1.3/jquery.validator.min.js?local=zh-CN',
        #'nice_validator_css': 'https://cdn.bootcss.com/nice-validator/1.1.3/jquery.validator.min.css',

        'adminlte': '/static/lib/adminlte2.4.10/dist/js/adminlte.min.js',
        'adminlte_css': '/static/lib/adminlte2.4.10/dist/css/AdminLTE.min.css',
        'adminlte_them_css':'/static/lib/adminlte2.4.10/dist/css/skins/_all-skins.min.css',        
        #'adminlte_css': 'https://cdn.bootcss.com/admin-lte/2.4.3/css/AdminLTE.min.css',
        #'adminlte_blue_css': 'https://cdn.bootcss.com/admin-lte/2.4.3/css/skins/skin-blue.min.css',
        
        #'nprogress': 'https://cdn.bootcss.com/nprogress/0.2.0/nprogress.min.js',
        #'nprogress_css': 'https://cdn.bootcss.com/nprogress/0.2.0/nprogress.min.css',
        
        #'element': 'https://cdn.bootcss.com/element-ui/2.4.0/index.js',  #'https://unpkg.com/element-ui/lib/index.js',
        #'element_css':'https://cdn.bootcss.com/element-ui/2.4.0/theme-chalk/index.css',  # 'https://unpkg.com/element-ui/lib/theme-chalk/index.css',
        #'md5': 'https://cdn.bootcss.com/blueimp-md5/2.10.0/js/md5.min.js',
        
        #'jb_admin_pack_js': '/static/js/jb_admin.pack.js?t=%s&t2=123'%js_stamp_dc.get('jb_admin_pack_js'),
        'jb_admin': static_url( 'js/jb_admin.pack.js?t=%s&t2=123'%js_stamp_dc.get('jb_admin_pack_js') ),
        #'fields':static_url( 'js/fields.pack.js?t=%s'%js_stamp_dc.get('fields_pack_js') ),  
        #'swiper': 'https://cdn.bootcss.com/Swiper/4.3.0/js/swiper.min.js',
        #'swiper_css': 'https://cdn.bootcss.com/Swiper/4.3.0/css/swiper.min.css',  
        'select2':'/static/lib/select2-4.0.10/dist/js/select2.min.js',
        'select2_css':'/static/lib/select2-4.0.10/dist/css/select2.min.css',
        
        'swiper': '/static/lib/swiper/js/swiper.min.js',
        'swiper_css': '/static/lib/swiper/css/swiper.min.css',  
        'echarts':'/static/lib/echarts.min.js',
        'chosen': '/static/lib/chosen_v1.8.7/chosen.jquery.min.js',
        'chosen_css': '/static/lib/chosen_v1.8.7/chosen.min.css',  
        'ckeditor': '/static/lib/ckeditor_4.10.1/ckeditor/ckeditor.js', 
        'notify':'https://cdn.jsdelivr.net/npm/@wcjiang/notify@2.0.12/dist/notify.min.js',
        'sortablejs':'https://cdn.jsdelivr.net/npm/sortablejs@1.8.4/Sortable.min.js',
        'selectizejs': 'https://cdn.jsdelivr.net/npm/selectize@0.12.6/dist/js/standalone/selectize.min.js', # 'https://cdn.jsdelivr.net/npm/selectize@0.12.6/dist/js/selectize.min.js',
        #'selectizejs_css':'https://cdn.jsdelivr.net/npm/selectize@0.12.6/dist/css/selectize.css',
        'selectizejs_css':'https://cdn.jsdelivr.net/npm/selectize@0.12.6/dist/css/selectize.default.css',
        'cropper_css':'/static/lib/cropper2.3.4.min.css',
        'cropper':'/static/lib/cropper2.3.4.min.js',
        # 这里需要更新
        'composition_api':'/static/lib/vue_lib/composition-api@1.0.0-rc.11',
        'vuedraggable':'https://cdn.jsdelivr.net/npm/vuedraggable@2.24.1/dist/vuedraggable.umd.min.js',# 'https://cdnjs.cloudflare.com/ajax/libs/Vue.Draggable/2.20.0/vuedraggable.umd.min.js'
    }
    if request.META['ACCESS_FROM_INTERNET']:

        dc.update( {
            'vuejs': 'https://cdn.jsdelivr.net/npm/vue@2.6.10/dist/vue.js',
            #'vuejs':   'https://cdn.jsdelivr.net/npm/vue@2.6.10/dist/vue.js',
            #'jquery':'https://cdn.jsdelivr.net/npm/jquery@2.2.4/dist/jquery.min.js',
            'jquery': 'https://cdn.jsdelivr.net/npm/jquery@3.4.1/dist/jquery.min.js',
            'vuex': 'https://cdn.jsdelivr.net/npm/vuex@3.0.1/dist/vuex.min.js', 
    
            'font_awesome': 'https://cdn.jsdelivr.net/npm/font-awesome@4.7.0/css/font-awesome.min.css',
            'bootstrap_css': 'https://cdn.jsdelivr.net/npm/bootstrap@3.3.7/dist/css/bootstrap.min.css',
            'bootstrap': 'https://cdn.jsdelivr.net/npm/bootstrap@3.3.7/dist/js/bootstrap.min.js',
            'layer': 'https://cdn.jsdelivr.net/npm/layerui@3.1.1/src/layer.min.js',
            'layer_css':'https://cdn.jsdelivr.net/npm/layerui@3.1.1/src/theme/default/layer.css', 
            'nice_validator': 'https://cdn.jsdelivr.net/npm/nice-validator@1.1.4/dist/jquery.validator.min.js?local=zh-CN',
            'nice_validator_css': 'https://cdn.jsdelivr.net/npm/nice-validator@1.1.4/dist/jquery.validator.css',
            'adminlte': 'https://cdn.jsdelivr.net/npm/admin-lte@2.4.10/dist/js/adminlte.min.js',
            'adminlte_css': 'https://cdn.jsdelivr.net/npm/admin-lte@2.4.10/dist/css/AdminLTE.min.css',
            #'adminlte_them_css':'https://cdn.jsdelivr.net/npm/admin-lte@2.4.10/dist/css/skins/skin-blue.min.css',
            'adminlte_them_css':'https://cdn.jsdelivr.net/npm/admin-lte-css@2.4.3/dist/css/skins/_all-skins.min.css',
            
            'nprogress': 'https://cdn.jsdelivr.net/npm/nprogress@0.2.0/nprogress.min.js',
            'nprogress_css': 'https://cdn.jsdelivr.net/npm/nprogress@0.2.0/nprogress.css',   
            
            #'element': 'https://cdn.jsdelivr.net/npm/element-ui@2.14.1/lib/index.js', 
            #'element_css':'https://cdn.jsdelivr.net/npm/element-ui@2.14.1/lib/theme-chalk/index.css',  
            'element': 'https://cdn.jsdelivr.net/npm/element-ui@2.15.7/lib/index.js', 
            'element_css':'https://cdn.jsdelivr.net/npm/element-ui@2.15.7/lib/theme-chalk/index.css',              
   
   
            'md5': 'https://cdn.jsdelivr.net/npm/blueimp-md5@2.10.0/js/md5.min.js',
            'swiper': 'https://cdn.jsdelivr.net/npm/swiper@4.5.0/dist/js/swiper.min.js',
            'swiper_css': 'https://cdn.jsdelivr.net/npm/swiper@4.5.0/dist/css/swiper.min.css',  
            'echarts':'https://cdn.jsdelivr.net/npm/echarts@4.9.0/dist/echarts.min.js',#'https://cdn.jsdelivr.net/npm/echarts@4.2.1/dist/echarts.min.js',
            'chosen':'https://cdn.jsdelivr.net/npm/chosen-js@1.8.7/chosen.jquery.min.js',
            'chosen_css':'https://cdn.jsdelivr.net/npm/chosen-js@1.8.7/chosen.min.css',
            #'ckeditor':'https://cdn.jsdelivr.net/npm/ckeditor@4.11.4/ckeditor.js',
            #'ckeditor':'https://cdn.jsdelivr.net/npm/ckeditor@4.11.4/ckeditor.min.js',
            'ckeditor': 'https://cdn.jsdelivr.net/gh/coblan/static@0.04/ckeditor_4.10.1/ckeditor/ckeditor.js',#'https://cdn.ckeditor.com/4.10.1/full/ckeditor.js',
            #'ckeditor':'https://cdn.jsdelivr.net/npm/ckeditor-full@4.7.3/ckeditor.js',
            
            'select2':'https://cdn.jsdelivr.net/npm/select2@4.0.10/dist/js/select2.min.js',
            'select2_css':'https://cdn.jsdelivr.net/npm/select2@4.0.10/dist/css/select2.min.css',
            
            'cropper_css':'https://cdn.jsdelivr.net/npm/cropper@4.1.0/dist/cropper.min.css',
            'cropper':'https://cdn.jsdelivr.net/npm/cropper@4.1.0/dist/cropper.min.js',
            'velocity':'https://cdn.jsdelivr.net/npm/velocity-animate@1.5.2/velocity.min.js',
            'animate_css':'https://cdn.jsdelivr.net/npm/animate.css@3.7.2/animate.min.css',
            'wow':'https://cdn.jsdelivr.net/npm/wow.js@1.2.2/dist/wow.min.js',
            'composition_api':'https://cdn.jsdelivr.net/npm/@vue/composition-api@1.5.0',
            'jsoneditor':'https://lib.baomitu.com/jsoneditor/9.7.4/jsoneditor.min.js',
            'jsoneditor_css':'https://lib.baomitu.com/jsoneditor/9.7.4/jsoneditor.min.css',
        })
        
        #if not settings.DEBUG:
            #dc.update({
                #'vue':'https://cdn.jsdelivr.net/npm/vue@2.6.10/dist/vue.min.js'
            #})
        
        if jsdeliver_crack:
            dc.update( {
                'vuejs': 'https://lib.baomitu.com/vue/2.6.14/vue.js',

                'jquery':'https://lib.baomitu.com/jquery/3.4.1/jquery.min.js',#  'https://lf9-cdn-tos.bytecdntp.com/cdn/expire-1-M/jquery/3.4.1/jquery.min.js',
                #'vuex': 'https://cdn.jsdelivr.net/npm/vuex@3.0.1/dist/vuex.min.js', 
        
                'font_awesome':'https://lib.baomitu.com/font-awesome/4.7.0/css/font-awesome.min.css', #'https://lf3-cdn-tos.bytecdntp.com/cdn/expire-1-M/font-awesome/4.7.0/css/font-awesome.min.css',
                'bootstrap_css': 'https://lib.baomitu.com/twitter-bootstrap/3.3.7/css/bootstrap.min.css',
                'bootstrap': 'https://lib.baomitu.com/twitter-bootstrap/3.3.7/js/bootstrap.min.js',
                
                'layer':'https://lib.baomitu.com/layer/3.1.1/layer.min.js',#  'https://lf6-cdn-tos.bytecdntp.com/cdn/expire-1-M/layer/3.1.1/layer.min.js',
                'layer_css': 'https://lib.baomitu.com/layer/3.1.1/mobile/need/layer.min.css',# 'https://lf9-cdn-tos.bytecdntp.com/cdn/expire-1-M/layer/3.1.1/mobile/need/layer.min.css', 
                'nice_validator':'https://lib.baomitu.com/nice-validator/1.1.4/jquery.validator.min.js?local=zh-CN',# 'https://lf9-cdn-tos.bytecdntp.com/cdn/expire-1-M/nice-validator/1.1.4/jquery.validator.min.js?local=zh-CN',
                'nice_validator_css':'https://lib.baomitu.com/nice-validator/1.1.4/jquery.validator.min.css',# 'https://lf3-cdn-tos.bytecdntp.com/cdn/expire-1-M/nice-validator/1.1.4/jquery.validator.min.css',
                'adminlte': 'https://lib.baomitu.com/admin-lte/2.4.18/js/adminlte.min.js',# 'https://lf26-cdn-tos.bytecdntp.com/cdn/expire-1-y/admin-lte/2.4.10/js/adminlte.min.js',
                'adminlte_css':'https://lib.baomitu.com/admin-lte/2.4.18/css/AdminLTE.min.css',# 'https://lf9-cdn-tos.bytecdntp.com/cdn/expire-1-y/admin-lte/2.4.10/css/AdminLTE.min.css',
                'adminlte_them_css': 'https://lib.baomitu.com/admin-lte/2.4.18/css/skins/_all-skins.min.css',# 'https://lf26-cdn-tos.bytecdntp.com/cdn/expire-1-y/admin-lte/2.4.10/css/skins/_all-skins.min.css',
                
                'nprogress': 'https://lib.baomitu.com/nprogress/0.2.0/nprogress.min.js',#  'https://lf6-cdn-tos.bytecdntp.com/cdn/expire-1-y/nprogress/0.2.0/nprogress.min.js',
                'nprogress_css':'https://lib.baomitu.com/nprogress/0.2.0/nprogress.min.css', # 'https://lf26-cdn-tos.bytecdntp.com/cdn/expire-1-y/nprogress/0.2.0/nprogress.min.css',   
                
    
                #'element': 'https://lib.baomitu.com/element-ui/2.15.8/index.min.js', 
                #'element_css':'https://lib.baomitu.com/element-ui/2.15.8/theme-chalk/index.min.css',    
                # 360总element可能显示icon有问题，替换成字节的
                #'element':'https://cdn.bytedance.com/cdn/expire-1-M/element-ui/2.15.7/index.min.js',
                #'element_css':'https://cdn.bytedance.com/cdn/expire-1-M/element-ui/2.15.7/theme-chalk/index.min.css',
                'element':'https://s1.pstatp.com/cdn/element-ui/2.15.7/index.min.js',
                'element_css':'https://s1.pstatp.com/cdn/element-ui/2.15.7/theme-chalk/index.min.css',                
                
       
                'md5': 'https://lib.baomitu.com/blueimp-md5/2.19.0/js/md5.min.js',
                'swiper': 'https://lib.baomitu.com/Swiper/4.5.1/js/swiper.min.js',
                'swiper_css': 'https://lib.baomitu.com/Swiper/4.5.1/css/swiper.min.css',  
                'echarts':'https://lib.baomitu.com/echarts/5.2.2/echarts.min.js',#'https://cdn.jsdelivr.net/npm/echarts@4.2.1/dist/echarts.min.js',
                'chosen':'https://cdn.jsdelivr.net/npm/chosen-js@1.8.7/chosen.jquery.min.js',
                'chosen_css':'https://cdn.jsdelivr.net/npm/chosen-js@1.8.7/chosen.min.css',

                'ckeditor': 'https://lib.baomitu.com/ckeditor/4.10.1/ckeditor.js',#
                'select2':'https://cdn.jsdelivr.net/npm/select2@4.0.10/dist/js/select2.min.js',
                'select2_css':'https://cdn.jsdelivr.net/npm/select2@4.0.10/dist/css/select2.min.css',
                
                'cropper_css':'https://cdn.jsdelivr.net/npm/cropper@4.1.0/dist/cropper.min.css',
                'cropper':'https://cdn.jsdelivr.net/npm/cropper@4.1.0/dist/cropper.min.js',
                'velocity':'https://cdn.jsdelivr.net/npm/velocity-animate@1.5.2/velocity.min.js',
                # 版本有兼容问题
                'animate_css':'https://lib.baomitu.com/animate.css/4.1.1/animate.min.css',
                #'animate_css':'https://lib.baomitu.com/animate.css/3.7.2/animate.min.css',
                'wow':'https://cdn.jsdelivr.net/npm/wow.js@1.2.2/dist/wow.min.js',
                #'composition_api':'https://cdn.jsdelivr.net/npm/@vue/composition-api@1.5.0',
                'composition_api':'/static/cdn/jb_admin/composition-api@1.6.0',
                ##'composition_api':'https://cdn.jsdelivr.net/npm/@vue/composition-api@1.6.1'
                'axios':'https://lib.baomitu.com/axios/0.26.1/axios.min.js',
                'ace':'https://lib.baomitu.com/ace/1.5.3/ace.min.js',
                'ace_javascript':'https://lib.baomitu.com/ace/1.5.3/mode-javascript.min.js',
   
            })
            if not settings.DEBUG:
                dc.update({
                    #'vue':'https://lib.baomitu.com/vue/2.6.10/vue.min.js',
                    'vuejs':'https://lib.baomitu.com/vue/2.6.14/vue.min.js',
                    #'vuejs_dev':'https://lib.baomitu.com/vue/2.6.14/vue.js', # 展示还没用，试试 vue.DEBUG=True
                })            
        
        # 由于早期没有ui_theme属性，方式用到了jb_admin作为管理界面的，默认加上skin-blue作为其主题
        #request.META['ENGIN'].ui_theme = request.META['ENGIN'].ui_theme or 'skin-blue'
        #if request.META['ENGIN'].ui_theme:
            #admin_theme_dc = {
                #'skin-black':'https://cdn.jsdelivr.net/npm/admin-lte@2.4.10/dist/css/skins/skin-black.min.css',
                #'skin-blue': 'https://cdn.jsdelivr.net/npm/admin-lte@2.4.10/dist/css/skins/skin-blue.min.css',
                #'skin-red': 'https://cdn.jsdelivr.net/npm/admin-lte@2.4.10/dist/css/skins/skin-red.min.css',
                #'skin-green': 'https://cdn.jsdelivr.net/npm/admin-lte@2.4.10/dist/css/skins/skin-green.min.css',
            #}
            #dc.update({
                #'adminlte_them_css':admin_theme_dc.get( request.META['ENGIN'].ui_theme  )
            #})
           
  
    return dc

js_lib_list.append(get_lib)