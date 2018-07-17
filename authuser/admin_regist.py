from helpers.director.shortcut import FieldsPage, ModelFields, director
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from .validate_code import faseGetDataUrl
from .models import  ValidatorCode
from .base_data import  auth_page_dc

class RegistFormPage(FieldsPage):
    template = 'authuser/regist_auth.html'
    class fieldsCls(ModelFields):
        field_sort = ['username', 'password', 'pswd2', 'validate_code', 'email']
        def __init__(self,  **kws): 
            instance = User()
            super().__init__(instance = instance, nolimit = True, **kws)
        
        def getExtraHeads(self): 
            #image, code = create_validate_code()
            #ValidatorCode.objects.create(code = code)
            
            #buffered = BytesIO()
            #image.save(buffered, format="JPEG")
            #img_str = base64.b64encode(buffered.getvalue())  
            
            #img_data_url = "data:image/jpeg;base64,%s" % img_str.decode('utf-8')
            
            return [
                {'name': 'pswd2','label': '确认密码','editor': 'password', 'required': True,'fv_rule': 'match(password)',}, 
                {'name': 'validate_code','label': '验证码',
                 'editor': 'com-field-validate-code',
                 'required': True,
                 'code_img': faseGetDataUrl(),}
                
            ]
        
        class Meta:
            model = User
            fields = ['username', 'password', 'email']
        
        def dict_head(self, head): 
            if head['name'] == 'password':
                head['editor'] = 'password'
            return head
    
        
        def clean_password(self):
            password = self.cleaned_data.get('password')
            
            if not password:
                raise forms.ValidationError(_('need password'))
            return password
        
        def clean_pswd2(self):
            password = self.data.get('password')
            pswd2 = self.cleaned_data.get('pswd2')
            if password != pswd2:
                raise forms.ValidationError(_('two password should be same'))
            return pswd2
            
        
        def clean_username(self):
            username = self.cleaned_data.get('username')
            if User.objects.filter(username=username).exists():
                raise forms.ValidationError(_('username has been exist'))
            return username

        def clean(self):
            if 'pswd2' in self.cleaned_data:
                del self.cleaned_data['pswd2']
            try:
                inst = ValidatorCode.objects.get(code = self.kw.get('validate_code'))
                inst.valid = False
                inst.save()
            except ValidatorCode.DoesNotExist:
                self._errors['validate_code'] = [_('Validate Code error')]
                #self.add_error('validate_code', _('Validate Code error'))
             
            return self.cleaned_data 
        
        def save_form(self): 
            super().save_form()
            user = self.instance
            user.set_password(user.password)
            user.is_active=True
            user.save()            
        
        
            

director.update({
    'authuser.regist': RegistFormPage.fieldsCls,
})
        

auth_page_dc .update({
    'regist': RegistFormPage,
})