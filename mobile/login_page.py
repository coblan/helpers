from . base_data import mb_page_dc
from helpers.mobile.fields import FieldsMobile,ModelFieldsMobile
from helpers.director.shortcut import FieldsPage,director,get_request_cache
from helpers.authuser.forms import LoginForm
from django.contrib import auth
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from helpers.director.base_data import js_tr_list
def get_tr():
    return {
        '请输入账号':_('请输入账号'),
        '请输入密码':_('请输入密码'),
        '登录':_('登录'),
    }
 
js_tr_list.append(get_tr)


class MobileLogin(FieldsPage):
    need_login=False
    
    def get_template(self):
        return 'mobile/live_show.html'
    
    def get_label(self):
        return _('用户登录')
    
    def get_context(self):
        ctx = super().get_context()
        dc = {
            'title':_('用户登录'),
            'after_save':'location=search_args.next;cfg.toast("%(login_success)s!")'%{'login_success':_("登录成功") },
            
        }
        if  getattr(self.engin,'can_regist',True):
            dc['footer'] =  [
                {'label':_('忘记密码'),'action':'cfg.toast("%(contact_admin)s")'%{"contact_admin":_("请联系管理员重置密码!")}},
                {'label':_('立即注册'),'action':'location="/mb/regist"'}
            ]

        ctx.update(dc)
        return {
            'editor_ctx':ctx,
            'editor': 'live_login', #'live_fields',
        }
    
    class fieldsCls(FieldsMobile):
        nolimit = True
        def get_heads(self):
            return [
                 {'name':'username','label':_('账号'),'editor':'com-field-linetext','required':True},
                 {'name':'password','label':_('密码'),'editor':'com-field-password','required':True},
            ]
        
        def get_operations(self):
            return [
                { 'name':'save','editor':'com-op-submit','label':_('登录'), 
                  'action':'scope.ps.vc.submit()'}
            ]
        
        def get_data_context(self):
            return {}
        
        def clean(self):
            username=self.kw.get('username')
            password=self.kw.get('password')

            if not username or not password:
                raise UserWarning(_('必须输入账号和密码') )
            user= auth.authenticate(username=username,password=password)  
            if user: 
                if user.is_active:
                    self.data_user = user
                else:
                    self.add_error('username',_('账号不可用'))
            else:
                try:
                    user=User.objects.get(username=username)
                    self.add_error('password',_('密码错误'))
                except User.DoesNotExist:
                    self.add_error('username',_('用户不存在'))
        
        def save_form(self):
            request = get_request_cache()['request']
            #user= auth.authenticate(username=self.kw.get( 'username') ,password=self.kw.get('password') )
            #if not auto_login:
                #request.session.set_expiry(0)
            auth.login(request, self.data_user)


director.update({
    'mb-login-form':MobileLogin.fieldsCls
})

mb_page_dc.update({
    'login':MobileLogin
})