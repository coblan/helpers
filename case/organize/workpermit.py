# encoding:utf-8

import json
from .models import WorkPermitModel
from helpers.director.model_admin.permit import ModelPermit,has_permit
from helpers.director.db_tools import model_to_name

class WorkModelPermit(ModelPermit):
    def __init__(self,model,user,department=None,nolimit=False):
        self.employee= user.employee_set.first()
        if not department:
            department=self.employee.depart_set.first()
        self.department=department        
        super(WorkModelPermit,self).__init__(model,user,nolimit=False)
        
        
    def _read_perm_from_db(self):
        model_name = model_to_name(self.model)
        workpermit= self.employee.workpermitmodel_set.filter(depart=self.department).first()
        for group in workpermit.group.all():
            if hasattr(group,'permitmodel'):
                permits = json.loads( group.permitmodel.permit )
                permit= permits.get(model_name,[])
                self.permit_list.extend(permit)
        self.permit_list=list(set(self.permit_list))    
    