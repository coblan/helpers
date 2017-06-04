# encoding:utf-8

from __future__ import unicode_literals
from __future__ import absolute_import

from helpers.director.shortcut import FormPage,TablePage,ModelFields,ModelTable,page_dc,model_dc,permit_list,TabGroup
from helpers.director.db_tools import to_dict
from django.contrib import admin
from .models import EmployeeModel,BasicInfo,Department
from django.contrib.auth.models import User
from django.db.models import Q
from helpers.common import employee
from helpers.common import department


class EmployeeFields(ModelFields):
    
    class Meta:
        model=EmployeeModel
        exclude=['baseinfo']
    
    def dict_options(self):
        users =list(User.objects.filter(employeemodel=None))
        if self.instance.user:
            users.append(self.instance.user)            
        return {
            'user':[{'value':user.pk,'label':unicode(user)}for user in users]
        }
    

class EmployeeItem(FormPage):
    template=''
    fieldsCls=EmployeeFields
    def get_template(self, prefer=None):
        return None
    def get_label(self):
        try:
            emp=EmployeeModel.objects.get(pk=self.pk)
            return '%s的工作信息'%(emp.baseinfo.name if emp.baseinfo else '未命名')
        except EmployeeModel.DoesNotExist:
            return '新建员工'

class BaseinfoItem(FormPage):
    template=''
    fieldsCls=BasicInfoFields
    def __init__(self, request):
        self.request=request
        pk= self.request.GET.get('pk')
        emp=EmployeeModel.objects.get(pk=pk)
        base,c = BasicInfo.objects.get_or_create(employeemodel__id=pk)
        if c:
            emp.baseinfo=base
            emp.save()
        self.emp=emp
        self.fields=self.fieldsCls(instance= base,crt_user=request.user)
        self.ctx=self.fields.get_context()
    
    def get_template(self, prefer=None):
        return None
    
    def get_label(self):
        return '%s的个人基本信息'%self.emp.baseinfo.name

class UserTab(UserFormPage):
    template=''
    fieldsCls=UserFields
    def __init__(self, request):
        self.request=request
        pk= self.request.GET.get('pk')
        emp=EmployeeModel.objects.get(pk=pk)
        user,c=User.objects.get_or_create(employeemodel__id=pk,defaults={'username':'_uid_%s'%pk})
        if c:
            emp.user=user
            emp.save()
        self.emp=emp
        self.fields=self.fieldsCls(instance= user,crt_user=request.user)
        self.ctx=self.fields.get_context() 
    
    def get_template(self, prefer=None):
        if prefer=='wx':
            return 'wx/tabgroup.html'
        else:
            return 'authuser/user_form_tab.html'
    def get_label(self):
        name = self.emp.baseinfo.name if self.emp.baseinfo else 'unnamed employee'
        return '%s的账号信息'%name

class EmpGroup(TabGroup):
    tabs=[{'name':'emp','label':'员工','page_cls':EmployeeItem},
          {'name':'baseinfo','label':'基本信息','page_cls':BaseinfoItem,'visible':and_list([BasicInfo])},
          {'name':'user','label':'账号','page_cls':UserTab,'visible':and_list([User])}]
    
    def get_tabs(self):
        emp_pk=self.request.GET.get('pk')
        if not emp_pk:      # 没有emp_pk 表示是新建employee
            tabs= self.tabs[0:1]
        else:
            
            tabs= self.tabs 
        tabs= evalue_container(tabs,user=self.request.user)
        return tabs

class EmployeeTable(ModelTable):
    model=EmployeeModel
    #exclude=['baseinfo']
    
    def dict_row(self, inst):
        dc={
            'user':unicode(inst.user),
            'baseinfo':unicode(inst.baseinfo),
            'head':inst.baseinfo.head if inst.baseinfo else ''
        }
        return dc        

class EmployeeTablePage(TablePage):
    tableCls=EmployeeTable 
    
    def get_label(self):
        return '员工列表'
    
class EmployeeTablePageWX(EmployeeTablePage):
    template='common/m_emp_table.html'

engine_dict={
    'employee':EmployeeTablePage,
    'employee.edit':EmpGroup,
    'employee.wx':EmployeeTablePageWX,
        'employee.wx.edit':EmpGroup,
    }