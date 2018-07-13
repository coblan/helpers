from helpers.director.shortcut import FieldsPage, ModelFields, director
from django.contrib.auth.models import User

class Regist(FieldsPage):
    template = 'authuser/regist_auth.html'
    class fieldsCls(ModelFields):
        def __init__(self,  **kws): 
            instance = User()
            super().__init__(instance = instance, nolimit = True, **kws)
            
        class Meta:
            model = User
            exclude = []
            

director.update({
    'authuser.regist': Regist.fieldsCls,
})
        

auth_page = {
    'regist': Regist,
}