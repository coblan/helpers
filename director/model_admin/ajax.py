# encoding:Utf-8
"""
这里的ajax函数是被所有由render生成的页面共用的。
如果TablePage或者FormPage的ajax_scope中有相同名字的函数，则优先调用。

"""
from __future__ import unicode_literals

from permit import ModelPermit
from base import model_dc
from ..db_tools import name_to_model,model_to_name,to_dict,permit_save_model
from fields import save_row
from django.core.exceptions import ValidationError
from ..models import PermitModel
from django.contrib.auth.models import Group,User
import json
#from base import model_dc,get_admin_name_by_model,del_row
from django.db import transaction

def model_perm(user,perm,model):
    validator = ModelPermit(model, user)
    return getattr(validator,perm)()


def save(row,user,request):
    """
    """
    try:
        field_obj = permit_save_model(user, row)
        dc = field_obj.get_row()
        # dc = save_row(row, user,request)
        # perm=ModelPermit(instance,user)
        # dc =to_dict(instance,include=perm.readable_fields())
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
        
def save_fieldset(fieldset,save_step,user):
    out={}
    try:
        with transaction.atomic():
            for step in save_step:
                if step.get('save'):
                    name=step.get('save')

                    fieldset[name] = save_row(fieldset.get(name), user)
                    instance=fieldset[name]
                    perm=ModelPermit(instance,user)
                    dc =to_dict(instance,include=perm.readable_fields())
                    out[name]=dc              
                      
                if step.get('assign'):
                    fieldset[step['obj']] [step['assign']]=fieldset[step['value']]
        return {'status':'success','fieldset':out}
    except ValidationError as e:
        return {'errors':dict(e),'path':name+'.errors'}     
    


def del_rows(rows,user):
    for row in rows:
        model = name_to_model(row.get('_class'))
        fields_cls = model_dc.get(model).get('fields')
        fields_obj = fields_cls(row,crt_user=user)
        fields_obj.del_form()
   
    return rows

#def save_group_and_permit(row,permits,user): 
    #field_cls = model_dc.get(Group).get('fields')
    #group_form= field_cls(row, crt_user= user)
    #if group_form.is_valid():
        #group_form.save_form()
    #group = group_form.instance
    #if not hasattr(group,'permitmodel'):
        #PermitModel.objects.create(group=group)
    #group.permitmodel.permit=json.dumps(permits)
    #group.permitmodel.save()
    
    ## perm={'group':group_form.instance.pk,'permit':permits}
    ## perm_form = save_row(perm, user)
    #return {'status':'success'}