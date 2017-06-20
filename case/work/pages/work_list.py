# encoding:utf-8

from __future__ import unicode_literals

from helpers.director.shortcut import ModelTable,TablePage
from ..models import WorkRecord
from helpers.case.organize.valid_depart import ValidDepart
from helpers.case.organize.workpermit import has_depart_permit

class WorkList(ModelTable):
    """
    拥有 work check all 权限的人，查看本部门的所有工作列表
    """
    model=WorkRecord
    
    def inn_filter(self, query):
        emp=self.crt_user.employee_set.first()
        valid_depart=WorkReadValidDepart(self.request)
        query_depart=valid_depart.get_query_depart()
        return query.filter(check_depart__in=query_depart)
  

class WorkReadValidDepart(ValidDepart):
    data_key='work_readall'
    def get_allowed_depart(self, employee, user):
        allowed_depart=[]
        for depart in employee.depart.all():
            if has_depart_permit(user, 'work.read_all', depart):
                allowed_depart.append(depart)
        return allowed_depart
    

class WorkListPage(TablePage):
    tableCls=WorkList
    template='work/work_list_wx.html'
    def get_context(self):
        ctx=super(WorkListPage,self).get_context()
        valid_depart=WorkReadValidDepart(self.request)
        ctx=valid_depart.get_context(ctx)
        return ctx
        


