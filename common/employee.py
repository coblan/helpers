# encoding:utf-8

from __future__ import unicode_literals

from django.contrib.auth.models import User,Group
from django.db import models
from django.utils.translation import ugettext as _
from . import human

from helpers.director.admin import UserFields,User,UserFormPage
from helpers.director.shortcut import FormPage,TablePage,ModelFields,TabGroup,ModelTable
# Create your models here.

class Employee(models.Model):
    user = models.ForeignKey(User,verbose_name=_('account'), blank=True, null=True)
    baseinfo=models.OneToOneField(human.HumanInfo,verbose_name=_('basic info'),blank=True,null=True)
    eid=models.CharField('employee id',max_length=30,default='')
   
    def __unicode__(self):
        if self.baseinfo:
            return self.baseinfo.name
        else:
            return 'unnamed employee'
    
    class Meta:
        abstract = True

def employee_admin( BasicInfo,
                    EmployeeModel):
   
    human_dc=human.get_admin(BasicInfo)
    BasicInfoFields=human_dc['BasicInfoFields'] 
    
    class EmployeeFields(ModelFields):
        
        class Meta:
            model=EmployeeModel
            exclude=[]
        
        def get_options(self):
            options= super(EmployeeFields,self).get_options()
            users = list(User.objects.filter(employeemodel=None))
            if self.instance.user:
                users.append(self.instance.user)
            options['user']=[{'value':user.pk,'label':unicode(user)}for user in users]
            return options  
    
    class EmployeeItem(FormPage):
        template=''
        fieldsCls=EmployeeFields
        def get_template(self, prefer=None):
            return None
    
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
            self.fields=self.fieldsCls(instance= base,crt_user=request.user)
            self.ctx=self.fields.get_context()
        
        def get_template(self, prefer=None):
            return None
    
    
    class UserTab(UserFormPage):
        template=''
        fieldsCls=UserFields
        def __init__(self, request):
            self.request=request
            pk= self.request.GET.get('pk')
            emp=EmployeeModel.objects.get(pk=pk)
            user,c=User.objects.get_or_create(employeemodel__id=pk)
            if c:
                emp.user=user
                emp.save()
            self.fields=self.fieldsCls(instance= user,crt_user=request.user)
            self.ctx=self.fields.get_context() 
        
        def get_template(self, prefer=None):
            if prefer=='wx':
                return 'wx/tabgroup.html'
            else:
                return 'authuser/user_form_tab.html'
    
    class EmpGroup(TabGroup):
        tabs=[{'name':'emp','label':'EMPLOYEE','page_cls':EmployeeItem},
              {'name':'baseinfo','label':'BASEINFO','page_cls':BaseinfoItem},
              {'name':'user','label':'ACCOUNT','page_cls':UserTab}]
        
        def get_tabs(self):
            if not self.request.GET.get('pk'):
                return self.tabs[0:1]
            else:
                return self.tabs   

    class EmployeeTable(ModelTable):
        model=EmployeeModel
        #exclude=['baseinfo']
        
        def dict_row(self, inst):
            dc={
                'user':unicode(inst.user),
                'baseinfo':unicode(inst.baseinfo)
            }
            return dc        
    
    class EmployeeTablePage(TablePage):
        tableCls=EmployeeTable 
    
    engine_dict={
        'employee':EmployeeTablePage,
        'employee.edit':EmpGroup,
        'employee.wx':EmployeeTablePage,
        'employee.wx.edit':EmpGroup,
    }
    
    return locals()