from helpers.director.shortcut import FieldsPage, ModelFields, director
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from .validate_code import faseGetDataUrl
from .models import  ValidatorCode
from .base_data import  auth_page_dc
from urllib.parse import unquote
from django.contrib import auth
from django.shortcuts import redirect
from helpers.director.middleware.request_cache import get_request_cache
from .forms import LoginForm

class LoginFormPage(FieldsPage):
    template = 'authuser/login.html'
    
    def get_heads(self): 
        return [
            {'name':'username','editor':'linetext','autofocus':True,'placeholder':'用户名'},
            {'name':'password','editor':'password','placeholder':'用户密码',},
        ]
    
    def get_context(self): 
        ctx = super().get_context()
        next_url= self.request.GET.get('next','/')
        dc={
            'page_cfg': {     
                'next':next_url,
                'title': '用户登录',
                'subtitle': '欢迎登录后台管理系统',
                #'regist_url': '%s/regist' % self.engin.engin_url,
                'copyright': 'Copyright @2018  All Right Reserve',
                'heads': self.get_heads(),
                'login_item': '用户名',
                },
        } 
        
        ctx.update(dc)
        return ctx
    
    @staticmethod
    def do_login(username,password,auto_login=False):
        """
        登录函数：
        """
        cache = get_request_cache()
        request = cache.get('request')
        form=LoginForm({'username':username,'password':password})
        
        if form.is_valid():
            user= auth.authenticate(username=username,password=password)
            if not auto_login:
                request.session.set_expiry(0)
            auth.login(request, user)
            return {'success':True,'token':request.session.session_key}
        else:
            return {'errors':form.errors}
        
    
    #class fieldsCls(ModelFields):
        #field_sort = ['username', 'password', 'pswd2', 'validate_code', 'email']
        #def __init__(self,  **kws): 
            #instance = User()
            #super().__init__(instance = instance, nolimit = True, **kws)
        
        
        #class Meta:
            #model = User
            #fields = ['username', 'password', 'email']
        
        #def dict_head(self, head): 
            #if head['name'] == 'password':
                #head['editor'] = 'password'
            #return head
    
        
        #def clean_password(self):
            #password = self.cleaned_data.get('password')
            
            #if not password:
                #raise forms.ValidationError(_('need password'))
            #return password
        
        #def clean_pswd2(self):
            #password = self.data.get('password')
            #pswd2 = self.cleaned_data.get('pswd2')
            #if password != pswd2:
                #raise forms.ValidationError(_('two password should be same'))
            #return pswd2
            
        
        #def clean_username(self):
            #username = self.cleaned_data.get('username')
            #if User.objects.filter(username=username).exists():
                #raise forms.ValidationError(_('username has been exist'))
            #return username

        #def clean(self):
            #if 'pswd2' in self.cleaned_data:
                #del self.cleaned_data['pswd2']
            #try:
                #inst = ValidatorCode.objects.get(code = self.kw.get('validate_code'))
                #inst.valid = False
                #inst.save()
            #except ValidatorCode.DoesNotExist:
                #self._errors['validate_code'] = [_('Validate Code error')]
                ##self.add_error('validate_code', _('Validate Code error'))
             
            #return self.cleaned_data 
        
        
            

#director.update({
    #'authuser.login': RegistFormPage.fieldsCls,
#})
        
class LogOutPage(object):
    def __init__(self, request, engin): 
        self.request = request
        self.engin = engin

    
    def get_context(self): 
        next = self.request.GET.get('next', self.engin.home)
        next=unquote(next)
        auth.logout(self.request)
        return redirect(next) 


director.update({
    'do_login': LoginFormPage.do_login,
})

auth_page_dc .update({
    'login': LoginFormPage,
    'logout': LogOutPage,
})