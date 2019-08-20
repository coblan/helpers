# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.models import Group,User
from helpers.director.shortcut import TablePage,ModelTable,page_dc,model_dc,ModelFields, director,RowFilter,director_view
from helpers.director.models import PermitModel 
from helpers.director.base_data import site_cfg
import re
from . import  js_cfg
from django.utils.translation import ugettext as _
from helpers.director.shortcut import model_to_name, model_full_permit, add_permits, model_read_permit,RowSearch
from django.db.models import Count
import json
# Register your models here.
class UserPage(TablePage):
    template='jb_admin/table.html'
    def get_label(self): 
        return _('User')
    
    class tableCls(ModelTable):
        model = User
        exclude=['password', 'last_name', 'user_permissions']
        pop_edit_field = 'username'
        fields_sort = ['id','username','first_name','groups','is_superuser','is_staff','is_active','last_login']
        
        def dict_head(self, head): 
            width={
                'username':120,
                'first_name':130,
                'groups':120,
            }
            if head['name'] in width:
                head['width'] = width.get(head['name'])
            if head['name'] == 'groups':
                head['label']='权限分组'
                head['editor'] = 'com-table-array-mapper'
                head['options'] = [{'value': group.pk, 'label': str(group),} for group in Group.objects.all()]
                #head['parse_method'] = 'dotSplit'
            if head['name'] == 'username':
                head['label']='账号'
            return head
        
        def inn_filter(self, query):
            if self.kw.get('groups_id'):
                return query.filter(groups__id =self.kw.get('groups_id'))
            else:
                return query
        
        class search(RowSearch):
            names=['username']
        class filters(RowFilter):
            names=['first_name','groups__name','is_superuser','is_staff','is_active']
            icontains=['first_name','groups__name']
            
            def getExtraHead(self):
                return [
                    {'name':'groups__name','label':'权限分组','show':'!scope.ps.search_args.groups_id'}
                ]
                
            
class UserFields(ModelFields):
    hide_fields = ['date_joined']
    class Meta:
        model=User
        fields=['username','first_name','is_active','is_staff','is_superuser','email','groups', 'date_joined']
    
    
    def dict_head(self, head):
        if head['name']=='groups':
            head['label']='权限分组'
            #head['editor']='field_multi_chosen'
            head['editor'] = 'com-field-multi-chosen'
        if head['name'] == 'username':
            head['label']='账号'
        return head

    def getExtraHeads(self):
        ls =[]
        if  'password' in self.permit.changeable_fields():
            ls.append({
                'name': 'user_password', 'label': '用户密码', 'editor': 'com-field-linetext', 'required': '!scope.row.pk',
                'fv_msg':'新建用户必须输入密码！','help_text':'如果填写,将会直接替换原来的用户密码'
            })
        return ls
    
    def clean_save(self): 
        if self.kw.get('user_password'):
            pswd =  self.kw.get('user_password')
            target_user = self.instance
            target_user.set_password(pswd)
            #target_user.save()            
            
        

class GroupPage(TablePage):
    template='jb_admin/table.html'
    
    def get_label(self): 
        return '权限分组'
    
    class tableCls(ModelTable):
        model=Group
        exclude=['permissions']
        pop_edit_fields=['name']
        #pop_edit_field = 'name'
        
        def inn_filter(self, query):
            return query.annotate(user_count = Count('user') )
        
        def getExtraHead(self):
            return [
                {'name':'user_count','label':'用户数'},
            ]
        
        #def dict_head(self, head):
            
            #if head['name']=='name':
                #groupform = GroupForm(crt_user=self.crt_user)
                #head['editor']='com-table-pop-fields'
                #head['get_row']={
                    #"fun":'use_table_row'
                #}
                #head['fields_ctx']=groupform.get_head_context()
                #head['after_save']={
                    ##'fun':'do_nothing'
                    #'fun':'update_or_insert'
                #}  
                #head['width'] = 200
                ##head['ops']=groupform.get_operations()

            ##if head['name']=='permissions':
                ##head['editor'] = 'com-field-ele-tree-name-layer'
                
            #return head
            
        def dict_head(self, head):
            width = {
                'name':300
            }
            if head['name'] in width:
                head['width'] = width.get(head['name'])
            if head['name'] =='user_count':
                head['editor'] = 'com-table-click'
                head['table_ctx'] =UserPage.tableCls().get_head_context()
                head['table_ctx'].update({
                    #'init_express':'ex.director_call(scope.vc.ctx.director_name,{car_no:scope.vc.par_row.car_no}).then(res=>ex.vueAssign(scope.row,res))',
                    #'after_save':'scope.vc.par_row.car_no =scope.row.car_no; scope.vc.par_row.has_washed=scope.row.has_washed ',
                    #'init_express':'cfg.show_load(),ex.director_call(scope.vc.ctx.director_name,{pk:scope.vc.par_row.pk}).then((res)=>{cfg.hide_load();ex.vueAssign(scope.row,res)})',
                    'init_express':'scope.ps.search_args.groups_id=scope.ps.par_row.pk;scope.ps.search()',
                    'ops_loc':'bottom'
                })
                head['action'] = 'scope.head.table_ctx.par_row=scope.row;cfg.pop_vue_com("com-table-panel",scope.head.table_ctx)'
            return head
    
        def dict_row(self, inst):
            dc ={}
            if inst.pk and hasattr(inst, 'permitmodel'):
                dc['permit']=[x for x in inst.permitmodel.names.split(';')]
            else:
                dc['permit']=[]
            dc.update({
                'user_count':inst.user_count
            })
            return dc
        

class GroupForm(ModelFields):
    field_sort = ['name']
    class Meta:
        model=Group
        exclude = []
       
        #fields=['name']
    
    #def dict_head(self, head):
        #if head['name']=='permissions':
            #head['editor'] = 'com-field-ele-tree-name-layer'   
        #return head
    
    def get_heads(self):
        heads= super(self.__class__,self).get_heads()
        options = site_cfg.get('permit.options')()
        #options = permit_dc.get('__root__')
        #options = [{'value':x.pk,'label':str(x)} for x in PermitModel.objects.all()]
        #options = list2tree(options)
        if director.get('permit.ui_options'):
            heads.append({
                'name':'ui',
                'editor':'com-field-select',
                'label':'权限视图',
                'options':director.get('permit.ui_options'),
                'help_text':'鉴于权限选择的复杂性和重要性，对权限进行了不同侧重点的整理，不同视图对应不同侧重点。',
                'event_slots':[
                    {'event':'input','express':'''cfg.show_load();
                     ex.director_call("permit.options",{ui:scope.event}).then((res)=>{cfg.hide_load();scope.ps.$emit("permit_options_changed", res)}) ''' },
                     #{'event':'input','express':'''
                     #var permit_head = ex.findone( scope.ps.vc.heads,{name:"permit"});
                     #cfg.show_load();
                     #ex.director_call("permit.options",{ui:scope.event}).then((res)=>{cfg.hide_load();permit_head.options=res}) ''' },
                    #{'event':'changed','express':'scope.ps.$emit("group-changed")'},
                ]
            })
        heads.append({
            'name':'permit',
            'editor':'com-field-ele-tree-depend',
            'label':'权限选择',
            'options':options,
            'event_slots':[
                {'par_event':'permit_options_changed','express':'scope.vc.refresh(scope.event)'},
            ]
        })
        return heads    
    
    def get_row(self):
        row=super(self.__class__,self).get_row()
        if self.instance.pk and hasattr(self.instance, 'permitmodel'):
            row['permit']=[x for x in self.instance.permitmodel.names.split(';')]
        else:
            row['permit']=[]
        return row   
    
    def clean_save(self):
        self.instance.save()
        if not hasattr(self.instance, 'permitmodel'):
            PermitModel.objects.create(group = self.instance)
        if self.kw.get('permit',None) != None:
            self.instance.permitmodel.names = ';'.join( self.kw.get('permit') ) 
            self.instance.permitmodel.save()

def list2tree(ls):
    clsfy = {}
    for i in ls:
        lb = i['label']
        mt = re.search('(.+)\.(.+)',lb)
        if mt:
            prefix,suffix = mt.group(1),mt.group(2)
            i['label'] = suffix
            if not clsfy.get(prefix):
                clsfy[prefix] =[]
            clsfy[prefix].append(i)
        else:
            clsfy[lb]= i 
    outer =[]
    for k,v in clsfy.items():
        
        if isinstance(v,list):
            dc = {'label':k,
                  'children':v}
        else:
            dc=v
        
        outer.append(dc)
    return outer
                

director.update({
    'jb_user': UserPage.tableCls,
    'jb_user.edit': UserFields,
    'jb_group': GroupPage.tableCls,
    'jb_group.edit': GroupForm,
})

page_dc.update({
    'jb_user':UserPage,
    'jb_group':GroupPage
})

def user_write(): 
    model = User
    fields = model._meta.get_fields()
    permit = {
        'read': [f.name for f in fields],
        'write': [f.name for f in fields if f.name != 'is_superuser'],
        '_can_create': True,
        '_can_delete': True,
    } 
    return json.dumps(permit)



permits = [('User.write', user_write(), model_to_name(User) , 'model'), 
           ('User.read', model_read_permit(User), model_to_name(User) , 'model'), 
           ('Group', model_full_permit(Group), model_to_name(Group) , 'model'), 
           ]

add_permits(permits)