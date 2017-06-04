# encoding:utf-8
from __future__ import unicode_literals

from django.contrib.auth.models import User,Group
from django.db import models
from django.utils.translation import ugettext as _
from helpers.common.employee import Employee
from helpers.common.human import HumanInfo
from helpers.common.department import DepartmentBase


class BasicInfo(HumanInfo):
    pass

class Department(DepartmentBase):
    pass

class EmployeeModel(Employee):
    baseinfo=models.OneToOneField(BasicInfo,verbose_name=_('basic info'),blank=True,null=True)
    position = models.CharField(_('job position'),max_length=100,blank=True)
    depart=models.ForeignKey(Department,verbose_name=_('department'),blank=True,null=True,on_delete=models.SET_NULL)

    class Meta:
        verbose_name=_('Employee Info')



