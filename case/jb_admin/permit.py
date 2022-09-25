from helpers.director.shortcut import model_to_name, model_full_permit, add_permits, model_read_permit
from django.contrib.auth.models import User,Group
import json

def user_write(): 
    model = User
    fields = model._meta.get_fields()
    permit = {
        'read': [f.name for f in fields],
        'write': [f.name for f in fields if f.name != 'is_superuser'],
        '_can_create': True,
        '_can_delete': True,
    } 
    return json.dumps(permit)

permits=[
    
   
    ('User.read', model_read_permit(User), model_to_name(User) , 'model'),   
    ('User.write', user_write(), model_to_name(User) , 'model'), 
    ('User.admin_page','','','single'),
    ('Group',model_read_permit(Group),model_to_name(Group),'model'),
    ('Group.edit', model_full_permit(Group), model_to_name(Group), 'model' ),         

    ]
add_permits(permits)

