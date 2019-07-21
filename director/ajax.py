# encoding:utf-8
from __future__ import unicode_literals
from .models import PermitModel
from .base_data import model_dc
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.conf import settings
import json
import os
from helpers.func.network.download_response import downloadfy_response

from .model_func.wirtedb import permit_save_model
from .model_func.dictfy import name_to_model,model_to_name,to_dict
import io
from helpers.director.base_data import director,director_views
from django.http import HttpResponse
from django.utils.timezone import datetime
from .fields.fields import ModelFields,OutDateException
from .network import argument

try:
    os.makedirs(os.path.join(settings.MEDIA_ROOT, 'gen_files'))
except:
    pass

def get_global():
    return globals()

def director_call(director_name, kws={}): 
    directorEnt= director_views.get(director_name)
    rt= directorEnt(**kws)
    if isinstance(rt,ModelFields):
        return rt.get_row()
    else:
        return rt

def save(row,user,request):
    """
    为了兼顾老的调用
    """
    return save_row(row, user, request)
    

def save_row(row,user,request):
    try:
        kw = request.GET.dict()
        field_obj = permit_save_model(user, row,**kw)
        dc = field_obj.get_row()
        return {'status':'success','row':dc}
    except ValidationError as e:
        return {'errors':dict(e)}
    except OutDateException as e:
        return {'_outdate':str(e)}


def get_new_row_ctx(model_name,user):
    model = name_to_model(model_name)
    fields_cls = model_dc[model].get('fields')
    return fields_cls(crt_user = user).get_context()
    
def get_row(director_name,pk=None,user=None,**kws):
    fields_cls = director.get(director_name)
    fields_obj = fields_cls(pk=pk,crt_user = user, **kws)
    return fields_obj.get_row()



def get_rows(director_name,search_args,user):
    table_cls = director.get(director_name)
    #model = name_to_model(model_name)
    #table_cls = model_dc[model].get('table')
    table_obj = table_cls.gen_from_search_args(search_args,user)
    return table_obj.get_data_context()

def get_excel(director_name,search_args,user): 
    table_cls = director.get(director_name)
    table_obj = table_cls.gen_from_search_args(search_args,user)
    wb = table_obj.get_excel()
    fl_name = director_name.replace('.', '_')
    now = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    fl_name =  '%s_%s.xlsx' % (fl_name, now)
    
    wb.save(filename = os.path.join(settings.MEDIA_ROOT, 'gen_files', fl_name))
    return {'file_url': '/media/gen_files/%s' % fl_name,}
    #response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    #response['Content-Disposition'] = 'attachment; filename=%s.xlsx' % fl_name
    #wb.save(response)
    #return response    

def save_rows(rows,user,request):
    kw=request.GET.dict()
    ls =[]
    try:
        for row in rows:
            field_obj = permit_save_model(user, row,**kw)
            dc = field_obj.get_row() 
            ls.append(dc)
        return ls
    
    except ValidationError as e:
        return {'errors':dict(e),}   
    except OutDateException as e:
        return {'_outdate':str(e)}

def del_rows(rows,user):
    for row in rows:
        fields_cls = director.get(row.get('_director_name'))
        #model = name_to_model(row.get('_class'))
        #fields_cls = model_dc.get(model).get('fields')
        fields_obj = fields_cls(row,crt_user=user)
        fields_obj.del_form()
    rows_only_pk=[{'pk':x['pk']} for x in rows]
    return rows_only_pk

def save_group_permit(row,user):
    field_obj = permit_save_model(user, row)
    inst = field_obj.instance
    exist_permitmodel = row.get('permit',[])
    for ee  in inst.permitmodel_set.exclude(pk__in=exist_permitmodel):
        inst.permitmodel_set.remove(ee)
    
    
    
def download_permit(items):
    pk_list=items.split('-')
    pk_list=[x for x in pk_list if x ]
    out=[]
    for permit in PermitModel.objects.filter(pk__in=pk_list):
        out.append({'name':permit.name,'permit':permit.permit,'desp':permit.desp})

    return downloadfy_response(json.dumps(out), 'permits.json')

def upload_permit(request):
    fl = request.FILES['file']
    catch = io.BytesIO()

    for chunk in fl.chunks():
        catch.write(chunk) 
    data=catch.getvalue()
    permits = json.loads(data)
    
    for permit in permits:
        permit_obj,_=PermitModel.objects.get_or_create(name=permit['name'])
        permit_obj.permit=permit['permit']
        permit_obj.desp=permit['desp']
        permit_obj.save() 
    return {'status':'success'}

def download_group(items):
    pk_list=items.split('-')
    pk_list=[x for x in pk_list if x ]
    out=[]
    for gp in Group.objects.filter(pk__in=pk_list):
        out.append({'name':gp.name,'permit':[x.name for x in gp.permitmodel_set.all()]})

    return downloadfy_response(json.dumps(out), 'group.json')   

def upload_group(request):
    fl = request.FILES['file']
    catch = io.BytesIO()

    for chunk in fl.chunks():
        catch.write(chunk) 
    data=catch.getvalue()
    groups = json.loads(data)
    for gp in groups:
        gp_obj,_=Group.objects.get_or_create(name=gp['name'])
        permits=PermitModel.objects.filter(name__in=gp['permit'])
        gp_obj.permitmodel_set.add(*list(permits))
        gp_obj.save()
    return {'status':'success'}