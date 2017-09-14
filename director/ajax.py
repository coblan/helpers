from models import PermitModel
from model_admin.base import model_dc
from django.contrib.auth.models import Group
import json
from .model_admin.ajax import *
from helpers.common.download_response import downloadfy_response
from helpers.director.db_tools import sim_dict,from_dict
import io

def get_global():
    return globals()

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

def download_group_permit(items):
    pk_list = items.split('-')
    pk_list=[x for x in pk_list if x ]
    str_list=[]
    for pk in pk_list:
        obj = Group.objects.get(pk=pk)
        
        if obj.permitmodel:
            if obj.name.startswith('assem.'):
                ls=json.loads(obj.permitmodel.permit)
                ls=[x.group.name for x in PermitModel.objects.filter(pk__in=ls)]
                dc={'group_name':obj.name,'permit_content':ls}
            else:
                dc={'group_name':obj.name,'permit_content':json.loads(obj.permitmodel.permit)}

            str_list.append(dc)
        
    return downloadfy_response(json.dumps(str_list), 'permits.json')

def upload_group_permit(request):
    fl = request.FILES['file']
    catch = io.BytesIO()
           
    for chunk in fl.chunks():
        catch.write(chunk) 
    data=catch.getvalue()
    group_permit = json.loads(data)
    
    assem_groups=[]
    other_groups=[]
    for gp in group_permit:
        if gp['group_name'].startswith('assem.'):
            assem_groups.append(gp)
        else:
            other_groups.append(gp)
    
    for gp in other_groups:
        name=gp['group_name']
        permit_content=json.dumps(gp['permit_content'])
        group,c = Group.objects.get_or_create(name=name)
        permitmodel,c=PermitModel.objects.get_or_create(group=group)
        permitmodel.permit=permit_content
        permitmodel.save()
    
    for gp in assem_groups:
        name=gp['group_name']
        permit_content=gp['permit_content']
        group,c = Group.objects.get_or_create(name=name)
        permitmodel,c=PermitModel.objects.get_or_create(group=group)
        
        permit_content=[x.pk for x in Group.objects.filter(name__in=permit_content)]
        permitmodel.permit=json.dumps(permit_content)
        permitmodel.save()
        
    return {'status':'success'}

def save_assem_group(row,user):
    
    group=from_dict(row)
    if not group.name.startswith('assem.'):
        group.name='assem.'+group.name
    group.save()
    permitmodel,c = PermitModel.objects.get_or_create(group=group)
    permitmodel.permit=json.dumps(row.get('child_group',[]))
    permitmodel.save()
    return {'status':'success'}