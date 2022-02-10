from helpers.director.shortcut import ModelFields,director
from django.contrib.auth.models import User

class PhoneRegist(ModelFields):
    class Meta:
        model = User
        fields=['username','password']
  
    def clean_save(self):
        user = self.instance
        user.set_password(self.kw.get('password'))
        user.is_active=True   
    
director.update({
    'edit/phone-regist':PhoneRegist
})