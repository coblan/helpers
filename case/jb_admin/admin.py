# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.models import Group,User
from helpers.director.shortcut import TablePage,ModelTable,page_dc,model_dc,ModelFields, director
from helpers.director.models import PermitModel 
from helpers.director.base_data import site_cfg
import re
from . import  js_cfg
from django.utils.translation import ugettext as _
from helpers.director.shortcut import model_to_name, model_full_permit, add_permits, model_read_permit,RowSearch

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
        #fields_sort = ['username']
        
        def dict_head(self, head): 
            if head['name'] == 'groups':
                head['label']='权限组'
                head['editor'] = 'com-table-array-mapper'
                head['options'] = [{'value': group.pk, 'label': str(group),} for group in Group.objects.all()]
                #head['parse_method'] = 'dotSplit'
            return head
        
        class search(RowSearch):
            names=['username']

class UserFields(ModelFields):
    hide_fields = ['date_joined']
    class Meta:
        model=User
        fields=['username','first_name','is_active','is_staff','is_superuser','email','groups', 'date_joined']
    
    
    def dict_head(self, head):
        if head['name']=='groups':
            head['label']='权限组'
            #head['editor']='field_multi_chosen'
            head['editor'] = 'com-field-multi-chosen'
        return head

    def getExtraHeads(self):
        ls =[]
        if  'password' in self.permit.changeable_fields():
            ls.append({
                'name': 'user_password', 'label': '用户密码', 'editor': 'password', 'required': '!scope.row.pk',
                'fv_msg':'新建用户必须输入密码！'
            })
        return ls
    #def get_heads(self): 
        #heads = ModelFields.get_heads(self)
        #if  'password' in self.permit.changeable_fields():
            #heads.append({
                #'name': 'user_password', 'label': '用户密码', 'editor': 'password', 'required': '!scope.row.pk',
            #})
        #return heads
    
    def clean_save(self): 
        if self.kw.get('user_password'):
            pswd =  self.kw.get('user_password')
            target_user = self.instance
            target_user.set_password(pswd)
            #target_user.save()            
            
        

class GroupPage(TablePage):
    template='jb_admin/table.html'
    
    def get_label(self): 
        return '用户角色组'
    
    class tableCls(ModelTable):
        model=Group
        exclude=['permissions']
        #pop_edit_field = 'name'
    
        def dict_head(self, head):
            
            if head['name']=='name':
                groupform = GroupForm(crt_user=self.crt_user)
                head['editor']='com-table-pop-fields'
                head['get_row']={
                    "fun":'use_table_row'
                }
                head['fields_ctx']=groupform.get_head_context()
                head['after_save']={
                    #'fun':'do_nothing'
                    'fun':'update_or_insert'
                }  
                head['width'] = 200
                #head['ops']=groupform.get_operations()

            #if head['name']=='permissions':
                #head['editor'] = 'com-field-ele-tree-name-layer'
                
            return head
    
        def dict_row(self, inst):
            dc ={}
            if inst.pk and hasattr(inst, 'permitmodel'):
                dc['permit']=[x for x in inst.permitmodel.names.split(';')]
            else:
                dc['permit']=[]
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
        heads.append({
            'name':'permit',
            'editor':'com-field-ele-tree-depend',
            'label':'权限选择',
            'options':options
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