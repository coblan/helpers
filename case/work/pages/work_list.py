# encoding:utf-8

from __future__ import unicode_literals

from helpers.director.shortcut import ModelTable,TablePage,FormPage,ModelFields
from ..models import WorkRecord
from helpers.case.organize.valid_depart import ValidDepart
from helpers.case.organize.workpermit import has_depart_permit
from helpers.director.db_tools import sim_dict

class WorkList(ModelTable):
    """
    拥有 work.read_all 权限的人，查看本部门的所有工作列表
    """
    model=WorkRecord
    
    def inn_filter(self, query):
        emp=self.crt_user.employee_set.first()
        valid_depart=WorkReadValidDepart(self.request)
        query_depart=valid_depart.get_query_depart()
        return query.filter(depart__in=query_depart).order_by('-id')
    
    def dict_row(self, inst):
        return {
            'emp':sim_dict(inst.emp.baseinfo),
            'work':unicode(inst.work),
            'depart':unicode(inst.depart)
        }
  
  

class WorkReadValidDepart(ValidDepart):
    data_key='work_readall'
    
    def get_allowed_depart(self):
        allowed_depart=[]
        for depart in self.employee.depart.all():
            if has_depart_permit(self.crt_user, 'work.read_all', depart):
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


class WorkListForm(ModelFields):
    class Meta:
        model=WorkRecord
        exclude=[]
    
    def get_heads(self):
        heads=super(WorkListForm,self).get_heads()
        for head in heads:
            if head.get('name')=='desp_img':
                head['type']='picture'
                head['config']={
                    'crop':True,
                'aspectRatio': 1,
                'size':{'width':250,'height':250}
                }
            elif head['name']=='finish_time':
                head['type']='date'            
            head['readonly']=True
        return heads

class WorkListFormPage(FormPage):
    fieldsCls=WorkListForm
    template='work/work_list_form_wx.html'


