from helpers.director.shortcut import director_view,get_request_cache,ModelFields
from helpers.director.decorator import need_login
from helpers.director.model_func.wirtedb import permit_save_model
from .models import User


class UserForm(ModelFields):
    simple_dict = True    
    nolimit = True
    class Meta:
        model = User
        exclude =['password','date_joined']

@director_view('user/info')
@need_login
def user_info(**row):
    request = get_request_cache()['request']
    user = request.user
    if request.method =='GET':
        return {
            'username':user.username,
            'nickname':user.first_name,
            'head':user.last_name,
            'email':user.email,
        }
    else:
        row['pk']=user.pk
        fields_obj = UserForm(dc = row,crt_user=user,)
        if fields_obj.is_valid():
            fields_obj.save_form()
        else:
            return  fields_obj.get_errors() 



