# encoding:utf-8

from helpers.director.db_tools import from_dict
from .models import WorkPermitModel,Employee,EmployeeData
import json

#from .models import Department
#from helpers.common.layer_tree import LayerTree
#import inspect
#from helpers.director.port import jsonpost


def get_global():
    return globals()

def save_self_info(base_info,user):
    """
    """
    instance = from_dict(base_info)
    instance.save()
    if getattr(instance,'employee',None) is None:
        emp =user.employee_set.first()
        emp.baseinfo=instance
        emp.save()
    elif instance.employee and instance.employee.user==user:
        instance.save()
    else:
        return {'status':'error','msg':'base info not match with current user'}
    return {"status":'success'}

def save_workpermit(permits,emp_pk,user):
    employee=Employee.objects.get(pk=emp_pk)
    for permit in permits:
        depart=from_dict(permit.get('depart'))
        wp=WorkPermitModel.objects.get(emp=employee,depart=depart)
        groups=[from_dict(x) for x in permit.get('groups') if x]
        #for group in groups:
            #wp.group.add(group)
        #for group in wp.groups.all():
            #if group not in groups:
                #wp.groups.remove(group)
        wp.group=groups
        wp.save()
    return {'status':'success'}

def save_emplyee_data(data_key,content,user):
    emp = user.employee_set.first()
    if not hasattr(emp,'employeedata'):
        EmployeeData.objects.create(emp=emp,content='{}')
    dc=json.loads(emp.employeedata.content)
    dc[data_key]=content
    emp.employeedata.content=json.dumps(dc)
    emp.employeedata.save()
    return {'status':'success'}


#def tree_department(request):
    #manager=LayerTree(Department)
    #scope= dict(inspect.getmembers(manager,inspect.ismethod))
    
    #if request.GET.get('get_class'):
        #return scope
    #else:
        #return jsonpost(request, scope)

