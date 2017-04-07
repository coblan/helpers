# encoding:Utf-8
"""
这里的ajax函数是被所有由render生成的页面共用的。
如果TablePage或者FormPage的ajax_scope中有相同名字的函数，则优先调用。

"""
from __future__ import unicode_literals

from permit import ModelPermit
from base import model_dc
from ..db_tools import name_to_model,model_to_name,to_dict
from fields import save_row
from django.core.exceptions import ValidationError
from ..models import PermitModel
from django.contrib.auth.models import Group,User
import json
#from base import model_dc,get_admin_name_by_model,del_row


def get_globle():
    return globals()


def model_perm(user,perm,model):
    validator = ModelPermit(model, user)
    return getattr(validator,perm)()


def save(row,user):
    """
    """
    try:
        instance = save_row(row, user)
        perm=ModelPermit(instance,user)
        dc =to_dict(instance,include=perm.readable_fields())
        return {'status':'success','row':dc}
    except ValidationError as e:
        return {'errors':dict(e)}
    #model= name_to_model(row['_class'])
    #fields_cls = model_dc.get(model).get('fields')

    #fields_obj=fields_cls(row,crt_user=user)
    #if fields_obj.is_valid():
        #return fields_obj.save_form()
    #else:
        #return {'errors':fields_obj.errors}


def del_rows(rows,user):
    for row in rows:
        model = name_to_model(row.get('_class'))
        fields_cls = model_dc.get(model).get('fields')
        fields_obj = fields_cls(row,crt_user=user)
        fields_obj.del_form()
   
    return rows

def save_group_and_permit(row,permits,user): 
    field_cls = model_dc.get(Group).get('fields')
    group_form= field_cls(row, crt_user= user)
    if group_form.is_valid():
        group_form.save_form()
    group = group_form.instance
    if not hasattr(group,'permitmodel'):
        PermitModel.objects.create(group=group)
    group.permitmodel.permit=json.dumps(permits)
    group.permitmodel.save()
    
    # perm={'group':group_form.instance.pk,'permit':permits}
    # perm_form = save_row(perm, user)
    return {'status':'success'}