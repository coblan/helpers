# encoding:utf-8

from __future__ import unicode_literals

from helpers.director.shortcut import ModelTable,TablePage
from ..models import WorkRecord

class WorkList(ModelTable):
    """
    拥有HEAD权限的人，查看本部门的所有工作列表
    """
    model=WorkRecord
    
    def inn_filter(self, query):
        emp=self.crt_user.employee_set.first()
        if emp and emp.depart:
            return query.filter(check_depart=emp.depart)
        else:
            return query.none()
        

class WorkListPage(TablePage):
    tableCls=WorkList


