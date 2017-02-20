# encoding:Utf-8
"""
这里的ajax函数是被所有由render生成的页面共用的。
如果TablePage或者FormPage的ajax_scope中有相同名字的函数，则优先调用。

"""
from __future__ import unicode_literals

from permit import Permit
from base import model_dc
from ..db_tools import name_to_model
from fields import save_row
from django.core.exceptions import ValidationError
#from base import model_dc,get_admin_name_by_model,del_row


def get_globle():
    return globals()


def model_perm(user,perm,model):
    validator = Permit(model, user)
    return getattr(validator,perm)()


def save(row,user):
    """
    """
    try:
        instance = save_row(row, user)
        return {'status':'success','pk':instance.pk,'_class':model_to_name(instance)}
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
   
    return {'status':'success','rows':rows}  