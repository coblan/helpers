from helpers.director.shortcut import FieldsPage, ModelFields, director,director_view
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from .models import PasswordInfo
from django.utils import timezone

from helpers.director.network import argument
from helpers.func.dot_dict import read_dict_path
from .base_data import  auth_page_dc
from django.conf import settings
from helpers.case.act_log.shortcut import operation_log
class AuthPwsd(FieldsPage):
    template = 'authuser/changepswd.html'
    need_login = False
    def get_context(self): 
        
        ctx = super().get_context()
        name = self.request.GET.get('username')
        if not name and self.request.user.is_authenticated():
            name= self.request.user.username
        dc={
            #'site_base_template': 'authuser/base.html',
            'login_url':'/%s/login' % self.engin.engin_url,
            'username':name,
            'uid':self.request.user.pk
        }   
        
        ctx.update(dc)
        return ctx
    
        

#director.update({
    #'authuser.login': RegistFormPage.fieldsCls,
#})
        
@director_view('authuser.changepswd')
def changepswd(row):
    if row.get('first_pswd')!=row.get('second_pswd'):
        return  {'errors':{'second_pswd':['两次密码不一致']}}
    elif not row.get('first_pswd'):
        return {'errors':{'first_pswd':['新密码不能为空!']}}
    
    if  read_dict_path(settings,'AUTHUSER.complex_password',False) :
        argument.validate_argument(row,{
            'first_pswd':[argument.complex_password]
        })
    md_user= User.objects.get(pk=row.get('uid'))

    if md_user.check_password(row.get('old_pswd')):
        md_user.set_password(row.get('first_pswd'))
        md_user.save()
        
        pswd,created = PasswordInfo.objects.get_or_create(user=md_user)
        pswd.last_change = timezone.now()
        pswd.save()
        operation_log('用户修改密码成功')
        dc={'status':'success'}
    else:
        dc={'errors':{'old_pswd':['old password not match']}}

    return dc



auth_page_dc .update({
    'pswd': AuthPwsd,
})