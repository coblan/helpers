# encoding:utf-8
from __future__ import unicode_literals

from django.core.exceptions import PermissionDenied
from .models import Department,EmployeeData
import json
from helpers.director.db_tools import to_dict

class ValidDepart(object):
    data_key=''
    def __init__(self,request):
        self.request=request
        self.crt_user=request.user
        self.employee=self.crt_user.employee_set.first()
        # self.data_key=data_key
    
    def get_query_depart(self):
        depart=self.get_crt_depart()
        depart_list=[]
        if hasattr(self.employee,'employeedata') and  self.employee.employeedata.content:
            dc = json.loads(self.employee.employeedata.content)
            pk_list = dc.get(self.data_key,[])
            depart_list=[Department.objects.get(pk=x) for x in pk_list]
            depart_list=filter(lambda x: x.par_chain.startswith(depart.par_chain),depart_list)
        if depart not in depart_list:
            depart_list.append(depart)
            
        return depart_list
    
    
    def get_crt_depart(self):
        allowed_depart= self.get_allowed_depart(self.employee,self.crt_user)
        if not allowed_depart:
            raise PermissionDenied,'No Valid department'
        depart=None
        if self.request.GET.get('_depart'):
            
            for dep in allowed_depart:
                if unicode(dep.pk) ==self.request.GET.get('_depart'):
                    depart=dep
        else:
            depart=allowed_depart[0]
        
        if not depart:
            raise PermissionDenied,'No Valid department' 
        return depart

    def get_allowed_depart(self, employee, user):
        """
        """
        return []
        # allowed_depart=[]
        # for depart in employee.depart.all():
            # permit = WorkModelPermit(WorkRecord, user, department=depart)
            # if 'status' in permit.changeable_fields():
                # allowed_depart.append(depart)
        # return allowed_depart   
    
    def get_context(self,ctx=None):
        ctx = ctx or {}
        allowed_departs=self.get_allowed_depart(self.employee,self.crt_user)
        ctx['depart_list']=[{'pk':x.pk,'label':unicode(x)} for x in allowed_departs]
        ctx['crt_depart']=to_dict( self.get_crt_depart())
        ctx['data_key']=self.data_key
        ctx['child_depart_list']=[to_dict(x) for x in self.get_query_depart()[:-1]]
        return ctx   
    
    