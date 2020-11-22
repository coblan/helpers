from django.db.models import ForeignKey
from ..field_procs.foreignproc import ForeignProc
from decimal import Decimal
from .. .base_data import field_map
from helpers.director.middleware.request_cache import get_request_cache
from django.contrib.auth.models import Group,User

class CreateUser(ForeignKey):
    '''TODO: 想清楚 ，什么时候给  field.instance赋值当前用户 '''
    def __init__(self, *args, **kwargs): 
        #self.digits = kwargs.pop('digits', 2)
        super().__init__(to=User ,*args, **kwargs)


class CreateUserProc(ForeignProc):

    def clean_field(self,dc,name):
        "现在无法调用该函数，所以这里还需要考虑下。"
        if not dc.get(name):
            request =  get_request_cache()['request']
            dc[name] = request.user.pk
        return dc.get(name)
    
field_map.update({
    CreateUser:CreateUserProc
})