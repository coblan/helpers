from . base_data import mb_page_dc
from helpers.mobile.fields import FieldsMobile,ModelFieldsMobile
from helpers.director.shortcut import FieldsPage,director,get_request_cache
from helpers.authuser.forms import LoginForm
from django.contrib import auth
from django.contrib.auth.models import User
from helpers.authuser.admin_regist import RegistFormPage
class MobileRegist(FieldsPage):
    need_login=False
    
    def get_template(self):
        return 'mobile/live.html'
    
    def get_label(self):
        return '用户注册'
    
    def get_context(self):
        ctx = super().get_context()
        ctx.update({
            'title':'用户注册',
            #'init_express':'scope.row._director_name="mb-login-form"',
            #'after_save':'cfg.toast("登录成功");setTimeout(function(){location=search_args.next},1500)'
        })
        return {
            'editor_ctx':ctx,
            'editor': 'live_fields',
        }
    
    class fieldsCls(ModelFieldsMobile,RegistFormPage.fieldsCls):
        pass
        #field_sort = ['username', 'password', 'pswd2', 'validate_code', 'email']
        #def __init__(self,  **kws): 
            #instance = User()
            #super().__init__(instance = instance, nolimit = True, **kws)
        ##def get_heads(self):
            ##return [
                 ##{'name':'username','label':'账号','editor':'com-field-linetext','required':True},
                 ##{'name':'password','label':'密码','editor':'com-field-password','required':True},
            ##]
        #def getExtraHeads(self): 
            #return [
                #{'name': 'pswd2','label': '确认密码','editor': 'password', 'required': True,'fv_rule': 'match(password)',}, 
                #{'name': 'validate_code','label': '验证码',
                 #'editor': 'com-field-validate-code',
                 #'required': True,
                 #'code_img': faseGetDataUrl(),}
                
            #]

director.update({
    'mb-regist-form':MobileRegist.fieldsCls
})

mb_page_dc.update({
    'regist':MobileRegist
})