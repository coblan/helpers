# encoding:utf-8
from __future__ import unicode_literals
from helpers.director.shortcut import ModelFields,FormPage,ModelPermit,model_dc
from ..models import WorkPermitModel,Employee
from helpers.director.db_tools import to_dict
from django.contrib.auth.models import Group


#class BasicInfoFields(ModelFields):

    #class Meta:
        #model=BasicInfo
        #exclude=[]
    
    #def get_heads(self):
        #heads=super(BasicInfoFields,self).get_heads()
        #for head in heads:
            #if head.get('name')=='head':
                #head['type']='picture'
                #head['config']={
                #'crop':True,
                #'aspectRatio': 1,
                #'size':{'width':250,'height':250}
            #}
        #return heads



class EmployePermitTab(FormPage):
    template=''

    def __init__(self, request):
        self.request=request
        pk= self.request.GET.get('pk')
        self.emp=Employee.objects.get(pk=pk)
        out=[]
        for depart in self.emp.depart.all():
            permit,c = WorkPermitModel.objects.get_or_create(emp=self.emp,depart=depart)
            out.append({'groups':[to_dict(x) for x in permit.group.all()],
                        'depart':to_dict(permit.depart)})
        groups=[to_dict(x) for x in Group.objects.all()] 
        self.ctx={
            'permits':out,
            'groups':groups
        }
    
    
    def get_context(self):
        ##if self.fieldsCls:
        
        self.ctx['can_add']=True
        self.ctx['can_del']=True   
        self.ctx['can_log']=True
        
        perm = ModelPermit(WorkPermitModel,self.request.user)
        if perm.changeable_fields():
            self.ctx['can_edit']=True
        else:
            self.ctx['can_edit']=False
        
        self.ctx['app']='organize'
        self.ctx['page_label'] =self.get_label()
        return self.ctx    
    
    def get_template(self, prefer=None):
        if prefer=='wx':
            return 'organize/employee_permit_wx.html'
        else:
            return 'organize/employee_permit.html'
    
    def get_label(self):
        return '%s的工作权限'%self.emp.baseinfo.name
    


class WorkPermiForm(ModelFields):
    class Meta:
        model=WorkPermitModel
        exclude=[]
        
model_dc[WorkPermitModel]={'fields':WorkPermiForm}