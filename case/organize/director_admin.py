# encoding:utf-8

from __future__ import unicode_literals
from __future__ import absolute_import

from helpers.director.container import evalue_container
from helpers.director.admin import UserFields,User,UserFormPage
from helpers.director.engine import and_list
from helpers.director.shortcut import FormPage,TablePage,ModelFields,ModelTable,page_dc,model_dc,permit_list,TabGroup
from helpers.director.db_tools import to_dict
from django.contrib import admin
from .models import Employee,BasicInfo,Department
from django.contrib.auth.models import User
from django.db.models import Q
from .pages.myinfo import EmployeeSelf
from .pages.baseinfo import BaseinfoItem,BasicInfoFields

class EmployeeFields(ModelFields):
    
    class Meta:
        model=Employee
        exclude=['baseinfo']
    
    def get_row(self):
        row = super(EmployeeFields,self).get_row()
        if 'depart' in row.keys() and self.instance.depart:
            row['depart_obj']={'pk':self.instance.depart.pk,'name':self.instance.depart.name}
        return row
    
    def dict_head(self, head):
        if head['name']=='eid':
            head['readonly']=True
        return head
    
    def dict_options(self):
        users =list(User.objects.filter(employee=None))
        if self.instance.user:
            users.append(self.instance.user) 
        
        user_options=[{'value':None,'label':'---'}]
        options=[{'value':user.pk,'label':unicode(user)}for user in users]
        options=sorted(options,cmp=lambda x,y: cmp(x['label'],y['label']) )
        user_options.extend(options)
        return {
            'user':user_options,
            'depart':[],
        }
    
class EmployeeItem(FormPage):
    template=''
    fieldsCls=EmployeeFields
    def get_template(self, prefer=None):
        return None
    def get_label(self):
        try:
            emp=Employee.objects.get(pk=self.pk)
            return '%s的工作信息'%(emp.baseinfo.name if emp.baseinfo else '未命名')
        except Employee.DoesNotExist:
            return '新建员工'
        # 
    def get_template(self, prefer=None):
        if prefer=='wx':
            return 'organize/employee_form_wx.html'
        else:
            return 'organize/employee_form.html'



class UserTab(UserFormPage):
    template=''
    fieldsCls=UserFields
    def __init__(self, request):
        self.request=request
        pk= self.request.GET.get('pk')
        emp=Employee.objects.get(pk=pk)
        user,c=User.objects.get_or_create(employee__id=pk)
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
        tabs= self.tabs
        if not emp_pk:      # 没有emp_pk 表示是新建employee
            tabs= self.tabs[0:1]
        else:
            emp= Employee.objects.get(pk=emp_pk)
            if not emp.user:        # 没有账号时，不显示账号标签
                tabs=[x for x in tabs if x['name']!='user']
            
        tabs= evalue_container(tabs,user=self.request.user)
        return tabs

class EmployeeTable(ModelTable):
    model=Employee
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
    template='organize/employee_table_wx.html'


class DepartmentForm(ModelFields):
    class Meta:
        model=Department
        exclude=['par']
        
class DepartmentPage(object):
    template=''
    def __init__(self,request):
        self.request=request
        
    def get_context(self):
        departform = DepartmentForm(crt_user=self.request.user)
        self.ctx={
            #'app':'',
            'heads':departform.get_heads(),
            'can_edit':departform.permit.can_add(),
        }
        return self.ctx  
    def get_template(self,prefer=None):
        if prefer=='wx':
            return 'organize/department_wx.html'
        else:
            return 'organize/department.html'


page_dc.update({
    'organize.employee':EmployeeTablePage,
    'organize.employee.edit':EmpGroup,
    'organize.department':DepartmentPage,
    'organize.employee.wx':EmployeeTablePageWX,
    'organize.employee.wx.edit':EmpGroup,
    'organize.employeeself.wx':EmployeeSelf,
})

model_dc[Employee]={'fields':EmployeeFields}
model_dc[Department]={'fields':DepartmentForm}
model_dc[BasicInfo]={'fields':BasicInfoFields}