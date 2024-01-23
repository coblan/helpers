
from django.contrib import admin
from django.contrib.auth.models import Group,User
from helpers.director.shortcut import TablePage,ModelTable,page_dc,model_dc,ModelFields, director,RowFilter,director_view,director,\
     director_element,get_request_cache,SelectSearch
from helpers.director.models import PermitModel 
import re
from . import  js_cfg
from django.utils.translation import ugettext as _
from helpers.director.shortcut import model_to_name, model_full_permit, add_permits, model_read_permit,RowSearch
from django.db.models import Count,F
import json
from helpers.director.access.permit import user_permit_names,group_permit
from helpers.func.dot_dict import read_dict_path
from django.conf import settings
from helpers.func.collection import ex
# Register your models here.
class UserPage(TablePage):
    template='jb_admin/table_new.html'
    def get_label(self): 
        return  '账号管理' # _('User')
    
    class tableCls(ModelTable):
        model = User
        exclude=['password', 'last_name', 'user_permissions']
        pop_edit_fields = ['username']
        fields_sort = ['id','username','first_name','groups','is_superuser','is_staff','is_active','last_login']
        allow_delete = read_dict_path(settings,'JB_ADMIN.delete_user',False)
        allow_create =  read_dict_path(settings,'JB_ADMIN.create_user',True)
        def get_head_context(self):
            ctx = super().get_head_context()
            get_request_cache()['named_ctx'].update({
                'jb-user-tabs':[
                    {'name':'account',
                    'label':'基本信息',
                     'editor':'com-tab-form',
                     'mounted_express':'ex.vueAssign(scope.vc.row,scope.par_row)',
                     'fields_ctx':UserFields().get_head_context()}
                ]
            })
            return ctx
        
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
    
            if head['name'] == 'username':
                head['label']='账号'
                head['editor'] = 'com-table-click'
                head['click_express'] = "scope.ps.switch_to_tab({ctx_name:'jb-user-tabs',tab_name:'account',par_row:scope.row})"
            return head
        
        def inn_filter(self, query):
            if self.kw.get('groups_id'):
                return query.filter(groups__id =self.kw.get('groups_id'))
            else:
                return query
        
        class search(SelectSearch):
            names=['username','first_name','groups__name',]
            def get_option(self, name):
                #if name =='first_name':
                    #return {
                                #'value':name,
                                #'label':'用户手机'
                            #}
                if name =='groups__name':
                    return {'value':name,'label':'权限组'}
                else:
                    return super().get_option(name)
                
        class filters(RowFilter):
            names=['is_superuser','is_staff','is_active']
            #icontains=['first_name']
            range_fields = ['last_login']
            
            #def getExtraHead(self):
                #return [
                    #{'name':'groups__name','label':'权限分组','show':'!scope.ps.search_args.groups_id'}
                #]
        
@director_element('group.select')
class GroupSelect(ModelTable):
    model = Group
    exclude=[]
    def get_operations(self):
        return [
            {'name':'sss','label':'确定',
             'editor':'com-btn',
             'type':'success',
             'click_express':'var ps=ex.vueParStore(scope.ps.vc,{name:"com-backend-table"}); ps.vc.$emit("finish",scope.ps.vc.selected)'},
        ]


def user_dif_promit(user,group):
    names = list( user_permit_names(user) )
    #group = Group.objects.filter(id=groupid).first()
    if group:
        group_names_list =  list(  group_permit(group) )
        group_names_list_plus = set( [x for x in group_names_list if not x.startswith('-')] )
        return group_names_list_plus.difference(names)
    else:
        return []

def user_group_options(user=None):
    """
    不传user，就当成是超级用户。这个是为了简化，直接返回全部选项给form。只要用户可以配置账号分组，就让他可以全部选择分组，否则过于复杂。
    """
    out = []
    if  user and getattr(Group,'filterByUser',None):
        query = Group.filterByUser(user)
    else:
        query = Group.objects.all()
    if not user or user.is_superuser:
        for group in query.select_related('permitmodel').all():
            out.append({
              'id':group.id,
              'name':group.name,
              'desp':group.permitmodel.desp,
              '_label':group.name
            })
    else:
        names = list( user_permit_names(user) )
        names_plus = set( [x for x in names if not x.startswith('-')] )
        names_minus = set( [x for x in names if x.startswith('-')] )
        for group in query.select_related('permitmodel').all():
            group_names_list =  list(  group_permit(group) )
            group_names_list_plus = set( [x for x in group_names_list if not x.startswith('-')] )
            group_names_list_minus = set( [x for x in group_names_list if x.startswith('-')] )
            # -  约束权限，没办法计入。
            if  names_plus.issuperset(group_names_list_plus)  : #and  names_minus.issubset(group_names_list_minus):
                out.append({
                    'id':group.id,
                    'name':group.name,
                    'desp':group.permitmodel.desp,
                    '_label':group.name
                })
    return out

class UserFields(ModelFields):
    "具有权限性的创建和修改用户资料"
    #hide_fields = ['date_joined']
    const_fields =['date_joined']
    class Meta:
        model=User
        fields=['username','first_name','is_active','is_staff','is_superuser','email','groups']
    
    
    def dict_head(self, head):
        if head['name']=='groups':
            head['label']='权限分组'
            #head['editor'] = 'com-field-select'
            #head['multiple'] = True
            head['editor'] = 'com-field-table-select'
            head['table_heads'] =[{'name':'name','label':'权限组','width':'150px'},
                                  {'name':'desp','label':'描述','pre':True}]
            
            # 只要用户可以配置用户分组，就让他可以看到全部分组。如果按照以前的限制，返回用户权限包含的分组，那么超过他权限的分组，在form中
            # 显示会出问题。
            head['table_rows'] = user_group_options() #user_group_options(self.crt_user) #GroupPage.tableCls().get_rows()
            if  getattr(Group,'filterByUser',None):
                head['valid_values']  = [x.pk for x in Group.filterByUser(self.crt_user)]
            
            head['order'] = 100
            
        if head['name'] == 'username':
            head['label']='账号'
            head['help_text'] = '作为登录账号,只能填写字母,数字或者下划线(_),长度为2~50'
            head['fv_rule'] = 'length(2~50);regexp(^\w+$ , 只能有字母,数字和下划线)' #
            #express = ''
            #msg = ''
            #head['fv_rule']='length(2~50);express(%s , %s)'%( express.decode('utf-8'),msg.decode('utf-8'))
        if head['name'] =='is_superuser':
            can_change =  read_dict_path(settings,'JB_ADMIN.superuser_field_change',True)
            if not can_change:
                head['readonly'] = True
            elif not self.crt_user.is_superuser:
                head['readonly'] = True
        #if head['name'] =='is_staff': # 这个可以不要，因为is_staff不是true的话，根本就看不到界面。
            #if not self.crt_user.is_superuser and not self.crt_user.is_staff:
                #head['readonly'] = True
        return head

    def getExtraHeads(self):
        ls =[]
        if  'password' in self.permit.changeable_fields():
            ls.append({
                'name': 'user_password', 'label': '用户密码', 'editor': 'com-field-linetext', 'required_express': '!scope.row.pk',
                'fv_msg':'新建用户必须输入密码！','help_text':'原有密码已被隐藏。输入框留空,则不会修改原有密码;如填写,将会覆盖原有密码。'
            })
        return ls
    
    def dict_row(self, inst):
        if not inst.pk:
            return {
                'is_staff':True
            }
        else:
            return {}
        
    def clean_save(self): 
        if self.kw.get('user_password'):
            pswd =  self.kw.get('user_password')
            target_user = self.instance
            target_user.set_password(pswd)
            self.extra_log +=f'修改用户{target_user}密码'
            #target_user.save()      
            
        can_change_superuser =  read_dict_path(settings,'JB_ADMIN.superuser_field_change',True)
        if not can_change_superuser:
            if 'is_superuser' in self.changed_data:
                raise UserWarning('不能修改超级管理员属性')
            
        # 检查设置人的权限
        if not self.crt_user.is_superuser:
            if 'is_superuser' in self.changed_data:
                raise UserWarning('您不是超级管理员，不能修改超级管理员属性')
            
            if not self.crt_user.is_staff:
                raise UserWarning('您不是管理员，不能设置用户信息')
            if 'groups' in self.changed_data:
                """
                当前只判断了【当前用户】给【目标用户】添加group时，不能超过【当前用户】自身的权限。
                TODO:可能需要判断【当前用户】删除【目标用户】group时，不能让【当前用户】删除更高权限的分组。
                考虑到普通用户为【目标用户】分配组时，可能是在特殊的界面，例如本部门下。所以不太可能能直接操作所有用户的分组，就不能乱删除。
                所以占时不做这个TODO需求。
                """
                #self.kw.get('groups')
                allow_group = user_group_options(self.crt_user)
                allow_group_ids = [x['id'] for x in allow_group]
                current_group = set(self.kw.get('groups'))
                before_group = set(self.before_changed_data.get('groups'))
                add_group = current_group.difference(before_group)
                remove_group = before_group.difference(current_group)
                
                #current_group_left = change_group.symmetric_difference( self.before_changed_data.get('groups')  )
                
                for group_id in add_group:
                    if group_id not in allow_group_ids:
                        group_obj = Group.objects.filter(pk=group_id).first()
                        if group_obj:
                            dif_names = user_dif_promit(self.crt_user, group_obj)
                            raise UserWarning(f'不能分配权限组:{group_obj}。你的权限不能覆盖{dif_names}。')
                        else:
                            raise UserWarning(f'所设置的id={group_id}的权限组不存在')
        
                for group_id in remove_group:
                    if group_id not in allow_group_ids:
                        group_obj = Group.objects.filter(pk=group_id).first()
                        if group_obj:
                            dif_names = user_dif_promit(self.crt_user, group_obj)
                            raise UserWarning(f'不能移除该权限组:{group_obj}。你的权限不能覆盖该{dif_names}。')
                        else:
                            raise UserWarning(f'所设置的id={group_id}的权限组不存在')


class NoLimitUserForm(UserFields):
    """ 在某些场合可能会创建新的用户或者修改下级用户，但是又不需要创建人员权限过大，所以不能赋予其user.edit权限,
    所以你用这个nolimitUserForm创建和修改别的用户信息,
    很显然这个类不能有自己的dirctor_name,不能被前端调用，只能由后端代码调用"""
    nolimit = True
    
    @classmethod
    def get_director_name(cls):
        return UserFields.get_director_name()

 
class UserPicker(ModelTable):
    model = User
    exclude = []
    fields_sort=['id','username','first_name']
    def dict_head(self, head):
        width = {
            'username':160,
            'first_name':230
        }
        if head['name'] in width:
            head['width'] = width[head['name']]
        if head['name'] =='username':
            head['editor'] = 'com-table-foreign-click-select'
        return head
    
    def get_head_context(self):
        ctx = super().get_head_context()
        ctx.update({
            'init_express':'scope.ps.search()',
            'ops_loc':'bottom'
        })
        return ctx
    
    class filters(RowFilter):
        names=['username','first_name']
        icontains = ['username','first_name']

class GroupPage(TablePage):
    template='jb_admin/table_new.html'
    
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
                {'name':'desp','label':'描述','editor':'com-table-pre'},
                {'name':'user_count','label':'用户数'},
                
            ]
        
        def get_operation(self):
            ops = super().get_operation()
            if read_dict_path(settings,'JB_ADMIN.export_permit',True):
                ops += [
                    {'name':'export_group',
                     'label':'导出权限分组',
                     'editor':'com-btn',
                     'click_express':'''
                     if(scope.ps.selected.length==0){var msg="确定要导出全部权限分组?"} 
                     else{var msg="确认要导出这"+scope.ps.selected.length + "个权限分组?"}
                     cfg.confirm(msg).then(()=>{
                         cfg.show_load();
                         debugger;
                         return ex.director("GroupExport").export( {groups:ex.map(scope.ps.selected,item=>{return item.pk })} )
                     }).then((permit_list)=>{
                         cfg.hide_load();
                         ex.saveLocalFile(JSON.stringify(permit_list),'groups.json')
                     })'''},
                    {'name':'export_group',
                     'label':'导入权限分组',
                     'editor':'com-btn',
                     'click_express':'''ex.readLocalFile(".json").then((text)=>{
                        var groups = JSON.parse(text)
                        cfg.show_load();
                        return ex.director("GroupExport").import_( {groups:groups} )
                     }).then(()=>{
                        cfg.hide_load();
                        scope.ps.search()
                     }) ''' },
                ]
            return ops

        def dict_head(self, head):
            width = {
                'name':300,
                'desp':400,
            }
            if head['name'] in width:
                head['width'] = width.get(head['name'])
            if head['name'] =='user_count':
                head['editor'] = 'com-table-click'
                head['table_ctx'] =GroupUserList().get_head_context()
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
                'user_count':inst.user_count,
                'desp':inst.permitmodel.desp,
            })
            return dc

class GroupUserList(UserPage.tableCls):
    def dict_head(self, head):
        if head['name'] == 'username':
            return head
        else:
            return super().dict_head(head)
    def get_operation(self):
        return [
        ]
    
    @classmethod
    def get_edit_director_name(cls):
        return UserPage.tableCls.get_edit_director_name()

@director_element('GroupExport')
class GroupExport(object):
    def export(self,groups=None):
        if groups:
            query = Group.objects.filter(pk__in=groups)
        else:
            query = Group.objects.all()
        outls = []
        for inst in query.annotate(permit=F('permitmodel__names')):
            outls.append({'id':inst.pk,'name':inst.name,'permit':inst.permit,'desp':inst.permitmodel.desp})
            #PermitModel
        return outls
    
    def import_(self,groups):
        for group in groups:
            inst,is_created = Group.objects.get_or_create(pk = group.get('id'))
            inst.name= group.get('name')
            inst.save()
            p_inst , is_created = PermitModel.objects.get_or_create(group= inst)
            p_inst.names = group.get('permit','')
            p_inst.desp = group.get('desp','')
            p_inst.save()
            
        


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
        options = director.get('permit.options')()
        ##options = permit_dc.get('__root__')
        ##options = [{'value':x.pk,'label':str(x)} for x in PermitModel.objects.all()]
        ##options = list2tree(options)
        if director.get('permit.ui_options'):
            heads.append({
                'name':'ui',
                'editor':'com-field-select',
                'label':'权限过滤',
                'options':director.get('permit.ui_options'),
                'help_text':'保存时会移除不在当前选择中的权限。不选择，代表所有权限都可选择',
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
        heads+= [
            {'name':'desp','label':'权限组描述','editor':'com-field-blocktext'},
        ]
        return heads    
    
    def get_row(self):
        row=super().get_row()
        if self.instance.pk and hasattr(self.instance, 'permitmodel'):
            row['permit']=[x for x in self.instance.permitmodel.names.split(';')]
        else:
            row['permit']=[]
        if hasattr(self.instance,'permitmodel'):
            row.update({
                'desp': self.instance.permitmodel.desp
            })
        return row   
    
    def clean_save(self):
        self.instance.save()
        
        #if not hasattr(self.instance, 'permitmodel'):
            #self.instance.permitmodel = PermitModel.objects.create(group = self.instance)
        self.instance.permitmodel.desp = self.kw.get('desp','')
        self.instance.permitmodel.save()
        if self.kw.get('permit',None) != None:
            before = {
                'permit':self.instance.permitmodel.names
            }
            
            # 原来设想的是把系统备选的有效权限缓存在class上，这样只需要提取一次。
            # 现在因为有 ui的影响，且操作权限并发不会太大，所以暂时不缓存。
            #if not getattr(self.__class__,'exposed_permit',None):
                #exposed_permit =[]
                #permit_options = director.get('permit.options')(self.kw.get('ui'))
                #for item in permit_options:
                    #exposed_permit += list( get_all_permit(item))
                #self.__class__ . exposed_permit = exposed_permit
            #else :
                #exposed_permit = self.__class__ . exposed_permit
                
            exposed_permit =[]
            permit_options = director.get('permit.options')(self.kw.get('ui'))
            for item in permit_options:
                exposed_permit += list( get_all_permit(item))
            
            valid_permit_ls = [x for x in self.kw.get('permit') if x in exposed_permit]
            self.instance.permitmodel.names = ';'.join( valid_permit_ls ) 
            self.instance.permitmodel.save()
            
            return {
                'before':before,
                'after':{
                    'permit':';'.join( valid_permit_ls ) 
                },
            }

# 以api的方式，可以给前端调用
@director_element('delete/usergroup')
@director_element('edit/usergroup')
class GroupFormUser(GroupForm):
    simple_dict = True


def get_all_permit(item):
    '获取所有暴露出来的permit'
    if item.get('value'):
        yield item.get('value')
    if item.get('children'):
        for child in item.get('children'):
            for dc in get_all_permit(child):
                yield dc



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
    'user.picker':UserPicker,
    'jb_group': GroupPage.tableCls,
    'jb_group.edit': GroupForm,
    'groupuserlist':GroupUserList,
})

page_dc.update({
    'jb_user':UserPage,
    'jb_group':GroupPage
})

