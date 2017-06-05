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


class EmployeeFields(ModelFields):
    
    class Meta:
        model=Employee
        exclude=['baseinfo']
    
    def get_row(self):
        row = super(EmployeeFields,self).get_row()
        if 'depart' in row.keys() and self.instance.depart:
            row['depart_obj']={'pk':self.instance.depart.pk,'name':self.instance.depart.name}
        return row
    
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
    template='organize/employee_form.html'
    fieldsCls=EmployeeFields
    def get_template(self, prefer=None):
        return None
    def get_label(self):
        try:
            emp=Employee.objects.get(pk=self.pk)
            return '%s的工作信息'%(emp.baseinfo.name if emp.baseinfo else '未命名')
        except Employee.DoesNotExist:
            return '新建员工'

class BasicInfoFields(ModelFields):

    class Meta:
        model=BasicInfo
        exclude=[]
    
    def get_heads(self):
        heads=super(BasicInfoFields,self).get_heads()
        for head in heads:
            if head.get('name')=='head':
                head['type']='picture'
                head['config']={
                'crop':True,
                'aspectRatio': 1,
                'size':{'width':250,'height':250}
            }
        return heads
    
class BaseinfoItem(FormPage):
    template=''
    fieldsCls=BasicInfoFields
    def __init__(self, request):
        self.request=request
        pk= self.request.GET.get('pk')
        emp=Employee.objects.get(pk=pk)
        base,c = BasicInfo.objects.get_or_create(employee__id=pk)
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
    template='common/m_emp_table.html'


class DepartmentForm(ModelFields):
    class Meta:
        model=Department
        exclude=['par']
        
class DepartmentPage(object):
    template='organize/department.html'
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


page_dc.update({
    'organize.employee':EmployeeTablePage,
    'organize.employee.edit':EmpGroup,
    'organize.department':DepartmentPage,
    'organize.employee.wx':EmployeeTablePageWX,
    'organize.employee.wx.edit':EmpGroup,
})

model_dc[Employee]={'fields':EmployeeFields}
model_dc[Department]={'fields':DepartmentForm}
model_dc[BasicInfo]={'fields':BasicInfoFields}