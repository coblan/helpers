# encoding:utf-8
from __future__ import unicode_literals
from django.db import models
from .dictfy import name_to_model,model_dc
from django.core.exceptions import ValidationError
from helpers.director.base_data import director
from helpers.director.fields.fields import OutDateException

def permit_save_model(user,row,**kw):
    for k in row: # convert model instance to pk for normal validation
        if isinstance(row[k],models.Model):
            row[k]=row[k].pk

    fields_cls = director.get(row['_director_name'])
    fields_obj = fields_cls(dc = row,crt_user=user,**kw)
    if fields_obj.is_valid():
        fields_obj.save_form()
        return fields_obj
    else:
        raise ValidationError(fields_obj.get_errors() )

    
