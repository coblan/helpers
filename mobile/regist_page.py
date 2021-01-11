from . base_data import mb_page_dc
from helpers.mobile.fields import FieldsMobile,ModelFieldsMobile
from helpers.director.shortcut import FieldsPage,director,get_request_cache
from helpers.authuser.forms import LoginForm
from django.contrib import auth
from django.contrib.auth.models import User
from helpers.authuser.admin_regist import RegistFormPage
from django.utils.translation import ugettext as _

class MobileRegist(FieldsPage):
    need_login=False
    
    def get_template(self):
        return 'mobile/live.html'
    
    def get_label(self):
        return _('用户注册')
    
    def get_context(self):
        ctx = super().get_context()
        ctx.update({
            'title':_('用户注册'),
            #'init_express':'scope.row._director_name="mb-login-form"',
            #'after_save':'cfg.toast("登录成功");setTimeout(function(){location=search_args.next},1500)'
        })
        return {
            'editor_ctx':ctx,
            'editor': 'live_fields',
        }
    
    class fieldsCls(ModelFieldsMobile,RegistFormPage.fieldsCls):
        nolimit=True
        class Meta:
            model = User
            fields = ['username', 'password', ]
        
        def dict_head(self, head): 
            if head['name'] == 'password':
                head['editor'] = 'com-field-password'
                head['fv_rule'] = _('密码:')
            if head['name']=='username':
                head['placeholder'] =_('用户名/手机号码')
            return head

director.update({
    'mb-regist-form':MobileRegist.fieldsCls
})

mb_page_dc.update({
    'regist':MobileRegist
})