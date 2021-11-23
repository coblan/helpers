from helpers.director.shortcut import FieldsPage, ModelFields, director,director_view
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
from helpers.director.kv import get_value,set_value,clear_value
from django.utils import timezone
from helpers.authuser.validate_code import code_and_url
from django.utils.translation import gettext as _
from django.conf import settings
from helpers.func.d_import import import_element

class LoginFormPage(FieldsPage):
    template = 'director/web.html'
    need_login = False # 如果不设置这里，engine会不断的跳转到登录界面,无法执行后面的内容 
    need_staff = False # 不设置这里， engin跳不过去
    
    def getExtraJs(self,ctx):
        return ['authuser']
    def get_context(self):
        return {
            'editor':getattr(self.engin,'login_com', 'login-form-jb'),
            'editor_ctx':{
                
            }
        }
    
   
#class LoginFormPage(FieldsPage):
    #template = 'authuser/login.html'
    #need_login = False # 如果不设置这里，engine会不断的跳转到登录界面,无法执行后面的内容 
    #need_staff = False # 不设置这里， engin跳不过去
    #def get_heads(self): 
        #return [
            #{'name':'username','editor':'linetext','autofocus':True,'placeholder':_('用户名')},
            #{'name':'password','editor':'password','placeholder':_('用户密码'),},
        #]
    
    #def get_context(self): 
        #ctx = super().get_context()
        #next_url= self.request.GET.get('next','/')
        #dc={
            #'page_cfg': {     
                #'next':next_url,
                #'title': _('用户登录'),
                #'subtitle': _('欢迎登录后台管理系统'),
                ##'regist_url': '%s/regist' % self.engin.engin_url,
                #'copyright': 'Copyright @%s  All Right Reserve'%timezone.now().year,
                #'heads': self.get_heads(),
                #'login_item': _('用户名'),
                #},
        #} 
        
        #ctx.update(dc)
        #return ctx
    

@director_view('username/login')
def login(username , password):
    row={"username":username,'password':password}
    rt= run(row)
    if 'errors' in rt:
        dc ={}
        for k,v in rt['errors'].items():
            dc[k] = ';'.join(v)
        rt['errors'] = dc
    return rt


@director_view('do_login')
def run(row):
    """
    为了实现token登录，需要添加中间件
    MIDDLEWARE = [
       'helpers.director.middleware.tokenuser.TokenUser',
       ...
    ]

    ##调用接口登录

    ```
    
    [POST]    /dapi/do_login     
    
        参数:
        {"username":"xx","password":"xxx"}
    
        返回:
        {
            "data": {
                "token": "i7u62v4o5340950xt3jguyilxgmodvxp",
                "success": true
            },
            "success": true
        }
     ```
    
     用户登录后，有多种方式携带登录信息进行其他api的请求。
           
     1. 直接用cookies。后台已经自动设置和http请求的cookies，如果携带cookies请求，可以直接请求其他api接口。
     
     2. 采用token。如果传递cookies有困难，直接将token放在http的header中，进行请求.字段名为 `Authorization:token`
     
     3. 如果设置header有困难，可以直接挂在url上请求，例如 : `api_url?token=xxx`
     
     
     **跨域问题**
     
     在浏览器中肯会存在跨域问题。后端进行了设置是允许跨域请求的，但是浏览器默认是不允许传递cookies等敏感信息，所以需要进行一定的设置。
     以jquery的请求为例,需要设置`withCredentials: true`
             
     ``` 
         $.ajax({
             url: a_cross_domain_url,
             xhrFields: {
                 withCredentials: true
             }
         });
     ```
    """    
    if getattr(settings,'DIRECTOR_LOGIN_BACKEND',None):
        loginClass = import_element(settings.DIRECTOR_LOGIN_BACKEND)
        loger = loginClass(row)
    else:
        loger = Login(row)

    if not loger.check_code():
        code,url = code_and_url()
        set_value(loger.code_key, code)
        return {'success':False,'errors':{'validate_code':[_('验证码错误')]},'validate_img':url}
    rt= loger.check_and_login()
    return rt

class Login(object):

    def __init__(self,row):
        self.request = get_request_cache()['request']
        self.row = row
        self.code_key = 'validate_code_user_%(username)s'%self.row
        self.count_key = 'login_count_user_%(username)s'%self.row
        self.code_life = timezone.now()-timezone.timedelta(minutes=30)

    def check_code(self):
        org_code = get_value(self.code_key,gte=self.code_life) # 30分钟内
        if  org_code:
            if  org_code.lower() != self.row.get('validate_code','').lower():
                return False
        return True

    def check_and_login(self):
        form=LoginForm({'username':self.row.get('username'),'password':self.row.get('password')})
        if form.is_valid():
            user= auth.authenticate(username=self.row.get('username'),password=self.row.get('password'))
            return self.login(user)
        else:
            return self.wrap_fail_info({
                'errors':form.errors
            })

    def login(self,user):
        if not self.row.get('auto_login'):
            self.request.session.set_expiry(0)  # 浏览器关闭就过期，否则默认是2星期过期
            #self.request.session['auto_login'] = False
        #else:
            #self.request.session['auto_login'] = True
            #self.request.session.set_expiry(0)settings.LOGIN_SPAN) 

        auth.login(self.request, user)

        clear_value(self.count_key)
        clear_value(self.code_key)
        
        return {'success':True,
                'token': self.request.session._get_or_create_session_key() ,# self.request.session.session_key
                }


    #def w(self,errors):
        #dc ={}
        #if not redisInst6.get(self.count_key) :
            #redisInst6.set(self.count_key,1,ex=60*60*2)
        #else:
            #old_value = redisInst6.get(self.count_key) 
            #redisInst6.set(self.count_key,int(old_value)+1,ex=60*60*2)

        #if int( redisInst6.get(self.count_key) ) >5:
            #code,url = code_and_url()
            #redisInst6.set(self.code_key,code,ex=60*3)
            #dc.update( {'success':False,'validate_img':url} ) 
        #dc.update({
            #'errors':errors
        #})
        #return dc
    
    def wrap_fail_info(self,infodc):
        old_count = int( get_value(self.count_key,0,gte=self.code_life) )
        old_count = old_count + 1
        set_value(self.count_key,old_count)
        
        if old_count >5:
            code,url = code_and_url()
            set_value(self.code_key,code)
            infodc.update( {'validate_img':url} )
        infodc.update({
            'success':False
        })
        return infodc
    
#@director_view('do_login')
#def do_login(row):
    #"""
    #登录函数：
    #"""
    #username = row.get('username')
    #password = row.get('password')
    #auto_login = row.get('auto_login',False)
    #cache = get_request_cache()
    #request = cache.get('request')
    #form=LoginForm({'username':username,'password':password})
    
    #if form.is_valid():
        #user= auth.authenticate(username=username,password=password)
        #if not auto_login:
            #request.session.set_expiry(0)
        #auth.login(request, user)
        #return {'success':True,'token':request.session.session_key}
    #else:
        #return {'errors':form.errors}
        
@director_view('do_logout')
def do_logout(**kw):
    request = get_request_cache()['request']
    auth.logout(request)
    
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


#director.update({
    #'do_login': LoginFormPage.do_login,
#})

auth_page_dc .update({
    'login': LoginFormPage,
    'logout': LogOutPage,
})