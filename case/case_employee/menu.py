# encoding:utf-8
from __future__ import unicode_literals

from helpers.director.engine import BaseEngine,can_list,can_touch,fa,page
from .models import BasicInfo,Employee,Department

pc_menu={
    'label':'员工管理','icon':fa('fa-users'),'visible':can_list((BasicInfo,Employee)),
        'submenu':[
                 {'label':'部门管理','url':page('case_employee_department'),'visible':can_touch(Department)},   
                 {'label':'员工名册','url':page('case_employee'),'visible':can_touch(Employee)},
    
             ]    
}