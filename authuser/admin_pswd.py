from helpers.director.shortcut import FieldsPage, ModelFields, director
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _


from .base_data import  auth_page_dc

class AuthPwsd(FieldsPage):
    template = 'authuser/changepswd.html'
    def get_context(self): 
        ctx = super().get_context()
        name= self.request.user.username
        dc={
            'login_url':'/%s/login' % self.par_url,
            'username':name,
            'uid':self.request.user.pk
        }   
        
        ctx.update(dc)
        return ctx
    
        

#director.update({
    #'authuser.login': RegistFormPage.fieldsCls,
#})
        

auth_page_dc .update({
    'pswd': AuthPwsd,
})