# encoding:utf-8
from __future__ import unicode_literals
from django.db import models
from .dictfy import name_to_model,model_dc
from django.core.exceptions import ValidationError,ObjectDoesNotExist
from helpers.director.base_data import director
from helpers.director.fields.fields import OutDateException
from django.db import transaction

def permit_save_model(user,row,**kw):
    for k in row: # convert model instance to pk for normal validation
        if isinstance(row[k],models.Model):
            row[k]=row[k].pk

    fields_cls = director.get(row['_director_name'])
    if not fields_cls:
        raise ObjectDoesNotExist('director:%s not exist'%row['_director_name'] )
    fields_obj = fields_cls(dc = row,crt_user=user,select_for_update=True,**kw)
    if fields_obj.is_valid():
        #with transaction.atomic():  # 现在 transaction 由外部请求参数控制，因为有可能有不可逆转的情况，
        #                              例如在save_form里面调用了三方api，在本地保存了api返回情况。这是即便是本地报错，也不能回退。
        fields_obj.save_form()
        return fields_obj
    else:
        raise ValidationError(fields_obj.get_errors() )

    
