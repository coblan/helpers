# encoding:utf-8
from __future__ import unicode_literals
from helpers.director.shortcut import ModelFields,FormPage
from ..models import BasicInfo,Employee

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