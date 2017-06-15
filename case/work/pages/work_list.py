# encoding:utf-8

from __future__ import unicode_literals

from helpers.director.shortcut import ModelTable,TablePage
from ..models import WorkRecord

class WorkList(ModelTable):
    model=WorkRecord
    
    def inn_filter(self, query):
        emp=self.crt_user.employee_set.first()
        if emp and emp.depart:
            return query.filter(check_depart__startswith=emp.depart.par_chain)
        else:
            return query.none()
        

class WorkListPage(TablePage):
    tableCls=WorkList


