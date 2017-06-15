# encoding:utf-8
from __future__ import unicode_literals
from __future__ import absolute_import

from ..models import Employee,BasicInfo
from .baseinfo import BasicInfoFields

class EmployeeSelf(object):
    template='organize/employee_self_wx.html'
    def __init__(self,request):
        user= request.user
        ctx={}
        emp= Employee.objects.filter(user=request.user).first()
        if not emp:
            ctx['no_emp']=True
        else:
            bf=BasicInfoFields(instance=emp.baseinfo,crt_user=user,nolimit=True)
            ctx['base_heads']=bf.get_heads()
            ctx['base_row']=bf.get_row()
            # ctx['root_page']=page('home.wx')('wx_engine')
        self.ctx=ctx
    
    def get_context(self):
        return self.ctx