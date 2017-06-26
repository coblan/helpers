# encoding:utf-8
from __future__ import unicode_literals

# from model_admin.render import TablePage,FormPage
from .pages import TablePage,FormPage
from model_admin.tabel import ModelTable
from model_admin.fields import ModelFields
from model_admin.base import model_dc,page_dc,permit_list
from django.contrib.auth.models import Group,User
import ajax
import json
from .model_admin.base import page_dc
from django.conf import settings
from .models import KVModel
from . import short_gen
import cgi

class UserGroupTable(ModelTable):
    model=Group
    include=['name']
    
    def inn_filter(self, query):
        return query.order_by('name')
        

class UserGroupFields(ModelFields):
    #template='user_admin/permit.html'
    class Meta:
        model=Group
        fields=['name',]
        
    def get_context(self):
        ctx = super(UserGroupFields,self).get_context()
        group = self.instance
        if hasattr(group,'permitmodel') and group.permitmodel.permit:
            ctx['permits']=json.loads(group.permitmodel.permit) #[{'model':x.model,'permit': json.loads(x.permit)} for x in self.instance.per.all()]
        else:
            ctx['permits']={}
        ctx['permit_heads']=self.permit.get_heads()
        return ctx

class GroupTablePage(TablePage):
    tableCls=UserGroupTable

class GroupFormPage(FormPage):
    template='form1/permit.html'
    fieldsCls=UserGroupFields
    ajax_scope=ajax.get_global()
    
class UserFields(ModelFields):
    class Meta:
        model=User
        fields=['username','first_name','is_active','is_staff','is_superuser','email','groups']

class UserTable(ModelTable):
    model=User
    include=['username','groups','first_name','is_active','is_staff','is_superuser','email',]
    
    #def get_rows(self):
        #rows=super(UserTable,self).get_rows()
        #for row in rows:
            #row['groups']=[group.name for group in Group.objects.filter(pk__in=row.get('groups'))]
        #return rows
    
    def dict_row(self, inst):
        return {
            'groups':';'.join([g.name for g in inst.groups.all()])
        }
        

class UserTablePage(TablePage):
    #template='authuser/user_table.html'
    tableCls=UserTable

class UserFormPage(FormPage):
    template='authuser/user_form.html'
    fieldsCls=UserFields

model_dc[Group]={'fields':UserGroupFields}
model_dc[User]={'fields':UserFields}



page_dc.update({'user':UserTablePage,
                'user.edit':UserFormPage,
                'group':GroupTablePage,
                'group.edit':GroupFormPage})

permit_list.append(Group)
permit_list.append(User)


class KVTable(ModelTable):
    model=KVModel
    exclude=[]
    def dict_row(self, inst):
        if len(inst.value)>50:
            value=inst.value[:50]+'...'
        else:
            value=inst.value
        return {
            'value':cgi.escape(value)
        }

class KvTablePage(TablePage):
    tableCls=KVTable

class KvFields(ModelFields):
    class Meta:
        model=KVModel
        exclude=[]

class KvFormPage(FormPage):
    fieldsCls=KvFields
    def get_template(self, prefer=None):
        if prefer=='wx':
            return 'wx/kvform.html'
        else:
            return 'director/kvform.html'

# short_gen.regist_director(['kv','kv.wx'],KVModel)
page_dc.update({
    'kv':KvTablePage,
    'kv.edit':KvFormPage,
})

model_dc[KVModel]={'fields':KvFields}