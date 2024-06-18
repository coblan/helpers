# encoding:utf-8
from __future__ import unicode_literals
from django import forms
from ..model_func.dictfy import form_to_head,to_dict, sim_dict,delete_related_query,model_to_name,from_dict,name_to_model,field_map,field_label
from django.http import Http404
import json
from django.db import models
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from ..base_data import model_dc
import base64
from django.db import models
from ..access.permit import ModelPermit
from helpers.director.base_data import director
from helpers.director.data_format.json_format import DirectorEncoder
from django.conf import settings
from django.utils.translation import ugettext as _
from helpers.director.middleware.request_cache import get_request_cache,request_cache
from helpers.func.collection.container import evalue_container
from django.db import transaction
import logging
from helpers.director.decorator import get_request_cache
from ..model_func.hash_dict import hash_dict,make_mark_dict,dif_mark_dict,adapt_type
from helpers.func.collection.ex import findone,find_index

# sql_log 可能没有什么用
#sql_log = logging.getLogger('director.sql_op')

modelfields_log = logging.getLogger('ModelFields.save_form')


class OutDateException(UserWarning):
    pass

class ModelFields(forms.ModelForm):
    """
    __init__函数，参数组合
    1. pk,crt_user 编辑，读取的时候
    2. instance,crt_user 编辑，读取的时候
    3. dc,crt_user 保存修改的时候。dc是新值组成的字典
    4. crt_user 新建的时候
    
    """
    readonly=[]
    readonly_all = False
    readonly_all_express = ''  # 前端执行为true时，整个com-form-one是只读的，save按钮也应该消失。
    const_fields=[]  # 只有创建的时候才允许修改的字段
    field_sort=[]
    extra_mixins=[]
    hide_fields = []
    overlap_fields=[]  # 这些字段不会被同步检查
    allow_overlap_all = False # 允许前端传递参数meta_overlap_fields=='__all__'，直接覆盖后端数据。现在默认数据很重要，不能随意覆盖。
    outdate_check_fields= None  # 功能应该与 overlaped_fields一致，只不过这个是正向的，相当于inlcude
    readonly_change_warning = [] # 普通保存时，后台会恢复只读字段的值，但是有时有些只读字段，
                                 #在后台发现改变时，需要警告前端，作废此次保存。因为这些字段值可能是前端做判断的依据。
    forbid_change = False # 禁止修改
    show_pk=False
    nolimit=False
    simple_dict = False
    allow_delete= False
    select_for_update = True  # 某些高频访问文件，写入不平凡，所以不允许锁定，就可以设置为False
    complete_field = True # False   # 自动补全没有上传的字段,在api或者selected_set_and_save中不必上传所有字段  2024/5/14改为true
    pass_clean_field = []
    allow_create = True
    foreign_bridge = []
    save_to_local= False
    front_info=True # 报错的时候，是否走前端的业务流程。例如 form 字段提醒，字段过期提醒等。
    
    @classmethod
    def parse_request(cls,request):
        """
        传入参数的形式：  
        被fieldsPage使用，最好不要再使用该函数，有点混乱了
        这个函数可能是被 d.get_row 使用的
        """
        dc=request.GET.dict()
        pk=dc.pop('pk',None)
        return cls(pk=pk,crt_user=request.user,select_for_update=False,**dc) 
    
    def __init__(self,dc={},pk=None,crt_user=None,select_for_update=True,*args,**kw):
        """
        调用情况：
        1. ajax save 时
        2. ajax get 时，获取数据，或者获取一个新的row数据。
        
        @dc: 当post save时 ,dc是前端传来的row字典。可以看到dc被传入了super函数,既传入了django.form中当做row参数。
                如果要设置instance的默认值，可以在kw中传入，这样第一次返回前端的时候就有值。
                如果在dc中传入默认值，第一次返回前端时，没有值，因为初始化时，不会调用 save_form 函数。
                
             当get 时，dc是前端传来的url参数中的dc字段，(基本上没有用）
        
        * 后端设置默认值:    1. 在clean_dict 中设置 ; 
                            2. 在clean_save中设置时，但是经历了 clean函数，可能验证不能通过
        * 前端设置默认值： 在 table的 add_new 操作中 添加 pre_set 。注意 foreignkey 需要加 _id
        
        """
        self.extra_log = ''
        
        if not crt_user:
            #self.crt_user=dc.get('crt_user')
            self.crt_user = get_request_cache()['request'].user
        else:
            self.crt_user = crt_user
            
        self.kw = kw.copy()
        # 修正参数
        
        # 2021/5/24 挪到这里
        dc = self._clean_dict(dc)
        dc=self.clean_dict(dc) 
        self.field_dc = dc
        if dc.get('instance'):
            self.kw['instance'] = dc.pop('instance')
        

            
        if pk is not None:
            pass
        elif dc.get('pk') != None and dc.get('pk') != '':
            pk=dc.get('pk')
        # 如果不注释这里会造成问题: 当前端手动输入id来创建记录，后端判断“是否新建”会错判为“不是新建”，产生找不到记录错误
        #elif dc.get('id') !=None and dc.get('id') != '': 
            #pk = dc.get('id')
        else:
            if self.kw.get('instance'):
                pk = self.kw['instance'].pk
            else:
                pk = None
        if not pk:
            self.is_create = True
        else:
            self.is_create = False 
           
        form_kw={}
        if 'instance' not in self.kw:
            if pk=='-1':  # -1 表示 最后一个记录 （一般用不到）
                form_kw['instance']= self.inn_filter( query= self._meta.model.objects.all()) .last()
            elif pk != None:  # 很多时候，pk=0 是已经创建了
                try:
                    if select_for_update and self.__class__.select_for_update:
                        form_kw['instance']= self.inn_filter( query= self._meta.model.objects.all().select_for_update()).get(pk=pk)
                    else:
                        form_kw['instance']= self.inn_filter(query= self._meta.model.objects.all() ).get(pk=pk)
                except self._meta.model.DoesNotExist:
                    raise UserWarning('Id=%s that you request is not exist'%pk)
                    # 感觉 instance不存在时，报错404可能不太合适，所以还是用普通报错 
                    #raise Http404('Id=%s that you request is not exist'%pk)
            else:
                # 前端初始化字段值，在 add_new opertions里面添加 pre_set:'rt={}'
                field_names = []
                for field in self._meta.model._meta.get_fields():
                    if isinstance(field,models.ForeignKey):
                        field_names.append('%s_id'%field.name)
                    else:
                        field_names.append(field.name)
                init_dc = {k:v for k,v in self.kw.items() if k in field_names}
                form_kw['instance'] = self._meta.model(**init_dc) #(**self.kw)
        else:
            form_kw['instance']=self.kw.pop('instance')
        
        self.custom_permit()
         # 强制 readonly的字段，不能修改
        inst =  form_kw['instance']
        
        # 如果row有meta_change_fields 字段，那么该次请求，只能修改这些字段，其他字段一律还原
        meta_change_fields=[]
        if dc.get('meta_change_fields'):
            meta_change_fields = dc.get('meta_change_fields').split(',')
        
        # 强制保存字段，不验证是否改变,并且其他字段都不能改变
        #if dc.get('meta_change_fields'):
            #force_change_fields = dc.get('meta_change_fields').split(',')
            #force_change_fields += self.overlap_fields
            #for k in self.permit.changeable_fields():
                #if k not in force_change_fields:
                    #fieldcls = inst.__class__._meta.get_field(k)
                    #if isinstance(fieldcls, models.ForeignKey):
                        #dc[k] = getattr(inst, "%s_id" % k)
                        #continue
                    #dc[k] = getattr(form_kw['instance'] , k)  kw
        

        # todict -> ui -> todict(compare) -> adapte_dict
        readonly_waring = []
        simdc = sim_dict(inst)  # 用来修正那些只读的字段
        orgin_simdc = dict(simdc)  # 将可json化的结果保存下来，后面记录日志会用到。simdc被clean处理过，可能不能json化了
            
        #n1 由于 multichoice.fullchoice, -1代表全部，出库的时候，转换为[1,2,3], 而数据库中是-1,造成数据库 出入不一致,所以加入以下_clean代码，将simdc再次还原为数据库数据。（simdc是走了to_dict转换函数的）
        #n2 TODO:可能会在以后移除这里的_clean_dict,因为应该保持数据库数据的 数据库->前端->后端 的一致性，就算显示需求，也应该利用_label等特殊字段。
        #【注意】 这里clean的是simdc,前面clean的外部传入的dc
        simdc = self._clean_dict(simdc)
        #simdc = self.clean_dict(simdc) 
        # 考虑到 self.readonly可能是property,可能不方便添加self.const_fields操作，所以用了一个新的变量readonly来进行操作。
        readonly = list( self.readonly )
        if not self.is_create:
            #readonly = list(self.readonly)
            readonly += self.const_fields
        
        if meta_change_fields or readonly:
            # 修正只读字段 
            for k in dict(dc):
                if k in readonly or (meta_change_fields and k not in meta_change_fields ):
                    if k in self.readonly_change_warning and adapt_type(dc[k]) != adapt_type( simdc.get(k)):
                        readonly_waring.append(k)
                    dc[k] = simdc.get(k)
                    if 'meta_org_dict' in dc:
                        dc['meta_org_dict'].pop(k,None)
                    #if hasattr(inst, "%s_id" % k):  # 如果是ForeignKey，必须要pk值才能通过 form验证
                        #fieldcls = inst.__class__._meta.get_field(k)
                        #if isinstance(fieldcls, models.ForeignKey):
                            #dc[k] = getattr(inst, "%s_id" % k)
                            #continue
                    #if hasattr(inst,k):
                        #dc[k] =  getattr(inst , k)  
        if readonly_waring : # and  not dc.get('meta_overlap_fields') == '__all__' : 这个有安全隐患 ，所以去掉
            raise OutDateException('(%s)的%s是只读的。但是已经发生了变化,请确认后再进行操作!'%(inst,[field_label(inst.__class__,k ) for k in readonly_waring] ) )
        
        # 真正的验证各个参数是否过期，是在clean函数中进行的。
        
        # 参数的修正挪到最上面
        #dc = self._clean_dict(dc)
        #dc=self.clean_dict(dc) 
        if self.complete_field and form_kw.get('instance'):
            dd = dict(simdc)
            dd.update(dc)
            dc = dd
        
        # 创建时，把必要的默认值补上 2024/5/14添加。
        # 原因： 在创建row时，某些隐藏字段是必填的，有默认值。
        # 后台创建是先从后台获取了默认row，再提交的，所以没有问题。
        # 但是三方api调用时，就会报错。
        if self.is_create:
            for field in self.Meta.model._meta.get_fields():
                if  dc.get(field.name) ==None and  hasattr(field,'blank') and field.blank != True:
                    if getattr(field,'default',None) !=None and field.default != models.fields.NOT_PROVIDED:
                        dc[field.name]= field.default

        self.kw.update(dc)        

        super(ModelFields,self).__init__(dc,*args,**form_kw)
        
        # 2023/8/14 加入bridge功能
        self.foreign_bridge_inst =[]
        for bridge in  self.foreign_bridge:
            self.foreign_bridge_inst.append( bridge.parseDict(dc,self.instance,crt_user=self.crt_user,select_for_update=self.select_for_update,*args,**kw) )
            
        # 2021-05-07 挪到上面
        #if not self.instance.pk:
            #self.is_create = True
        #else:
            #self.is_create = False
        #if not self.is_create:
            ## 有时候 self.changed_data 会错误包含其他字段
            ## 有问题，因为有些 foreignkey  或者 onetoone字段 读取的时候不存在，报异常
            #for name in list( self.changed_data ):
                #if getattr(self.instance,name) == dc.get(name):
                    #self.changed_data.remove(name)
        
        self.pop_fields()
        self.init_value()
        
        self.op_log={}
        
        # 保留下instance的原始值,用于记录日志;
        # 因为simdc被clean函数处理过，可能不能json化，所以使用 orgin_simdc。后面 orgin_simdc 用于保存日志
        self.before_changed_data = {k:v for k,v in orgin_simdc.items() if k in self.changed_data} # sim_dict(self.instance, include= self.changed_data)
       
        #self.org_db_dict = mark_dict(self.instance.__dict__,keys= self.fields.keys())
    
    def findInstance(self,dc):
        pass
    
    
    def inn_filter(self,query=None):
        if getattr(self._meta.model,'filterByUser',None):
            query = self._meta.model.filterByUser(user=self.crt_user,query=query) 
        return query
    
    
    
    def full_clean(self):
        rt = super().full_clean()
        if self.pass_clean_field:
            for k in self.pass_clean_field:
                if k in self._errors:
                    self._errors.pop(k) 
        return rt
    
    def clean(self):
        """
        数据过期检查
           overlaped_fields  用于排除掉不需要检查的字段。
           meta_key_fields   用于设定只检查哪些字段
           
           meta_change_fields 在__init__函数中，不在meta_change_fields中的字段会被还原，只剩下变化的，所以这里不需要检测了。
           
        """
        super().clean()         
        overlaped_fields = []
        if self.kw.get('meta_change_fields'): 
            return 
        if self.kw.get('meta_overlap_fields'):
            if self.kw.get('meta_overlap_fields') =='__all__' :
                if not self.allow_overlap_all:
                    raise UserWarning('overwrite data not allowed')
                # 表示覆盖所有字段，意味着不再做过期检查
                return
            overlaped_fields+= self.kw.get('meta_overlap_fields').split(',')
        if self.overlap_fields:
            overlaped_fields += self.overlap_fields
            
        if self.instance.pk and self.changed_data  and self.kw.get('meta_org_dict') : 
      
            crt_mark_dc= self.get_org_dict()
            
            # 这个太复杂了，转由后端控制。
            #if self.kw.get('meta_key_fields'):
                #meta_key_fields = self.kw.get('meta_key_fields').split(',')
                #dif_dc = dif_mark_dict(crt_mark_dc,self.kw.get('meta_org_dict'),include= meta_key_fields)
            if self.outdate_check_fields != None:
                dif_dc = dif_mark_dict(crt_mark_dc,self.kw.get('meta_org_dict'),include= self.outdate_check_fields)
            else:
                dif_dc = dif_mark_dict(crt_mark_dc, self.kw.get('meta_org_dict'),exclude= overlaped_fields)
            
            if dif_dc:
                key_labels =[]
                for key in dif_dc.keys():
                    fld =self.fields.get(key)
                    if fld:
                        key_labels.append(fld.label)
                        #key_labels.append(fld.verbose_name)
                        #keys.append(fld.label)
                    else:
                        # field中找不到，只能返回 key值
                        key_labels.append(key)
                        
                #keys = [self.fields.get(key).label for key in dif_dc.keys() ]
                raise OutDateException('(%s)的%s已经发生了变化,请确认后再进行操作!'%(self.instance, key_labels ) )
                #raise OutDateException('(%s)的%s已经发生了变化,请确认后再进行操作!'%(self.instance, [field_label(self.instance.__class__, x ) for x in keys]       ) )
    
    def get_org_dict(self,row=None):
        if not row:
            row = self.get_row()
        return make_mark_dict(row)
    
    def _clean_dict(self,dc):
        """利用field_map字典，查找前端传来的dc中，某个字段的转换方式"""

        ls = [x for x in dc.keys() if x.startswith('_')]
        for k in ls:
            dc.pop(k)
            
        model = self.Meta.model
        model_name = model_to_name(model)
        
        all_field_names =[f.name for f in model._meta.get_fields()]
        for k,v in dc.items():
            if not k.startswith('_'):
                if k in all_field_names:
                    field = model._meta.get_field(k)
                    if field_map.get(field.__class__):
                        mapper_cls = field_map.get(field.__class__)
                        dc[k] =  mapper_cls(field=field).clean_field(dc,k)
                        
                field_path = model_name+'.'+k
                if field_map.get(field_path):
                    map_cls = field_map[field_path]
                    field = model._meta.get_fields()
                    dc[k]=map_cls().clean_field(dc,k) 
        return dc
    
    def clean_dict(self,dc):   
        return dc
    
    def get_data_context(self):
        return {
            'row':self.get_row()
           }
    
    def is_valid(self): 
        rt = True
        for bridge,bridge_inst in zip(self.foreign_bridge,self.foreign_bridge_inst):
            rt = rt and bridge.isValid(bridge_inst)
        
        rt =  rt and super().is_valid()
        
        extra_errors = self.extra_valid()
        self._extra_errors =  extra_errors
        return rt and not extra_errors
    
    def extra_valid(self): 
        """在django的clean函数中，**自定义**的字段，raise ValidationError ，会被django清除掉，所以只能在后面重新验证"""
        return {}
        
    def get_errors(self): 
        extra_errors = getattr(self, '_extra_errors', {})
        
        errors = dict(self.errors)
        
        for k, v in extra_errors.items():
            if k in errors:
                errors[k].append(v)
            else:
                errors[k] = [v]
        
        for bridge,bridge_inst in zip(self.foreign_bridge,self.foreign_bridge_inst):
            errors.update( bridge.getErrors(bridge_inst) )       
        
        return errors
    
    def custom_permit(self):
        self.permit=ModelPermit(self.Meta.model,self.crt_user,nolimit=self.nolimit)
    
    @classmethod
    def get_director_name(cls):
        director_name = ''
        for k,v in director.items():
            if v==cls:
                director_name=k
                break
        return director_name    
    
    def get_context(self):
        """
        """
        ctx = self.get_head_context()
        ctx.update(self.get_data_context())
        return ctx
    
    @request_cache
    def get_head_context(self):
        heads = self.get_heads()
        ops =  self.get_operations()
        dc = {
            'heads':heads,
            'ops':ops,
            'director_name':self.get_director_name(),
            #'model_name':model_to_name(self._meta.model),
            'extra_mixins':self.extra_mixins,
            'allow_overlap_all':self.allow_overlap_all,
            'readonly_all_express':self.readonly_all_express,
        }   
        if self.save_to_local:
            dc['save_express' ] =  'scope.vc.$emit("finish",scope.vc.row);rt=Promise.resolve(scope.vc.row)'
        return dc
    
    
    def get_del_info(self):
        return {'%(model)s:%(inst)s <id=%(pk)s>'%{'model':self.instance.__class__.__name__,'inst':str(self.instance),'pk':self.instance.pk}:delete_related_query(self.instance)}
    
    def get_operations(self):
        ls=[]
        if self.permit.changeable_fields() and not self.forbid_change:
            ls += [
                {
                'name':'save',
                #'editor':'com-field-op-btn',
                'editor':'com-btn',
                'type':'primary',
                'icon':'el-icon-receiving',
                'label':'保存' if not self.save_to_local else '确定', 
                'click_express':'scope.ps.vc.submit()',
                'show_express':'''rt= ! scope.vc.ctx.readonly_all'''
                #'icon': 'fa-save',
                #'class':'btn btn-info btn-sm',
            },
                # 暂时屏蔽，需要考虑清楚 页面兼容性问题
                #{
                #'name':'save_and_return','editor':'com-field-op-btn','label':'保存后返回','icon':'fa-share-square','show':'scope.vc.back',
                #'class':'btn btn-sm','action':'scope.vc.submit().then((row)=>{ scope.vc.back()})'
                #}
            ]
        if self.allow_delete and self.permit.can_del():
            ls += [
                {
                'name':'delete',
                'editor':'com-btn',
                'type':'danger',
                'icon':'el-icon-delete',
                'label':'删除', 
                'click_express':'''(async ()=>{
                      cfg.show_load();
                      var resp = await ex.director_call("d.delete_query_related",{rows:[scope.ps.vc.row]})
                      cfg.hide_load();
                      if(resp.length>0){
                            cfg.pop_vue_com("com-pan-delete-query-message",{msg_list:resp,genStore:scope.ps,title:"删除关联确认"})
                       }else{
                            await cfg.confirm(`确认删除[${scope.ps.vc.row._label}]?`)
                            cfg.show_load()
                            await ex.director_call("d.delete_row",{row:scope.ps.vc.row})
                            cfg.hide_load()
                            cfg.toast("删除成功")
                       }
                       // tab形式的
                       var ps = ex.vueParStore(scope.ps.vc,{name:'com-widget-el-tab'})
                       if(ps){
                            var tab_table = ps.vc.ctx.genVc
                            tab_table.search()
                            cfg.switch_back()
                       }
                      
                })()
                ''',
                'show_express':'scope.row.pk'
                #'icon': 'fa-save',
                #'class':'btn btn-info btn-sm',
                      },
            ]
        if self.readonly_all:
            ls = []
        return ls
    
    def get_permit(self):
        """
        现在转换为控制按钮组，这个函数应该是没有用了。
        """
        permit_dc = {
            'can_add':self.permit.can_add(),
            'can_del':self.permit.can_del() ,
            'can_log':self.permit.can_log(),
            'can_edit':bool( self.permit.changeable_fields() )
        }

        return permit_dc
    
    def pop_fields(self):
        """
        pop some field out,this will be 
        """
        if self.nolimit or self.crt_user.is_superuser:
            return
        ls=[]
        ls.extend(self.permit.readable_fields())
        ls.extend(self.permit.changeable_fields())
        for key in dict(self.fields).keys():
            if key not in ls:
                self.fields.pop(key)
                
    
    def init_value(self):
        """可能是用于 foreignkey 或者 manytomany的"""
        if self.instance.pk != None:
            for field in self.instance._meta.get_fields(): #get_all_field_names():
                f=field.name
                if f in self.fields:
                    try:
                        value = getattr(self.instance,f)
                    except field.related_model.DoesNotExist as e:
                        value = None
                    if hasattr(value,'all'):
                        value=value.all()
                    self.fields[f].initial= value
    
    def getExtraHeads(self): 
        return []
    
    def _base_dict_fieldmap_heads(self): 
        out = []
        model_meta = self._meta.model._meta
        for k,v in self.fields.items():
            #if isinstance(include,(tuple,list)) and k not in include:
                #continue
            if k in self.hide_fields:
                continue
            
            dc = {'name':k,
                  'label': str( model_meta.get_field(k).verbose_name ) , # str(v.label),
                  'help_text':str(v.help_text),
                  'editor':'com-field-linetext'}
                  
            if hasattr(v,'required'):
                dc['required'] = v.required   
                     
            if hasattr(v,'widget') and isinstance(v.widget,forms.widgets.Select):
                dc['editor'] = 'sim_select' 
                #dc['options']=[{'value':val,'label':str(lab)} for val,lab in v.widget.choices]
            elif v.__class__==forms.fields.CharField:
                if v.max_length:
                    dc.update({'editor':'com-field-linetext','maxlength':v.max_length})
                else:
                    dc.update({'editor':'com-field-blocktext'})
            elif v.__class__==forms.fields.BooleanField:
                dc['editor']='bool'
                #dc['no_auto_label']=True
            elif v.__class__ in [forms.fields.IntegerField,forms.fields.FloatField]:
                dc['editor']='com-field-number'
            elif v.__class__  == forms.fields.DateField:
                dc['editor']='date'
            if v.__class__ ==forms.models.ModelMultipleChoiceField and \
                isinstance(v.widget,forms.widgets.SelectMultiple):
                dc['editor']='field_multi_chosen'
            
            
            
            model_field = self._meta.model._meta.get_field(k)
            fieldName = model_to_name(self._meta.model) + '.' + k
            if fieldName in field_map:
                mapper=field_map[fieldName]
                mapper(self.instance, name = k,model=self._meta.model).dict_field_head(dc)
            elif model_field.__class__ in field_map:
                mapper=field_map[model_field.__class__]
                mapper(self.instance, name = k,model=self._meta.model).dict_field_head(dc)    
                
            #dc = self.dict_head(dc)
            out.append(dc)
        return out
    
    @request_cache
    def get_heads(self):
        
        #heads = form_to_head(self)
        if self.show_pk:
            heads=[
                {'name':self._meta.model._meta.pk.name,'label':self._meta.model._meta.pk.verbose_name,'editor':'linetext','readonly':True}
            ]
        else:
            heads=[]
        heads += self._base_dict_fieldmap_heads()
        heads.extend(self.getExtraHeads())
        # 本来hide_fields只需要过滤model中的字段。但是某些时候继承，需要过滤掉getExtraHeads中增加的字段，所以在这里再次过滤一遍。
        heads = [x for x in heads if x['name'] not in self.hide_fields]
        heads = [self.dict_head(head) for head in heads]
        
        self.heads = heads
        # 设置前端组件的只读属性
        if self.forbid_change:
            for head in heads:
                head['readonly']=True 
        else:
            for name in self.get_readonly_fields():
                for head in heads:
                    if head['name']==name:
                        head['readonly']=True 
                        break
                
        for head in heads:
            if head.get('editor') == 'sim_select' and not head.get('options'):
                v = self.fields.get(head['name'])
                head['options']=[{'value':val,'label':str(lab)} for val,lab in v.widget.choices]
                if len(head['options']) > 300:
                    print('%s 选择项数目大于 300，请使用分页选择框' % head['name'])
                    break        
        
        if self.field_sort:
            tmp_heads = []
            for k in self.field_sort:
                for head in heads:
                    if head['name'] == k:
                        tmp_heads.append(head)
            heads=tmp_heads
        # [排序] 从下面挪上来，先排序，再处理after_fields
        heads = sorted(heads,key=lambda head: head.get('order',0))
        # start: 实现 after_fields 排序
        after_fields_list =[]
        after_dict = {}
        for head in heads:
            if head.get('after_fields'):
                after_fields_list.extend(head.get('after_fields'))
                after_dict[head['name']]=[] 
                for item in head.get('after_fields'):
                    item_head = findone(heads, {'name':item})
                    if item_head:
                        after_dict[head['name']].append(item_head)
                
        lefts = [x for x in heads if x['name'] not in after_fields_list ]
        for k,v in after_dict.items():
            index = find_index(lefts,{'name':k})
            lefts[index:index] = v       
            
        heads=evalue_container(lefts)
        for head in heads:
            if head['name']=='_meta_head':
                heads.remove(head)
                heads= [head]+heads
                break
        
        # 增加桥接
        for bridge,bridge_inst in zip(self.foreign_bridge,self.foreign_bridge_inst):
            heads += bridge.getHeads(bridge_inst,base_inst = self.instance)  
        
        # [排序] 挪到after_fields处理代码上面，先排序，在处理after_fields
        #heads = sorted(heads,key=lambda head: head.get('order',0))
        if self.readonly_all:
            for head in heads:
                head['readonly'] =True
        return heads
    
    def can_access(self):
        """
        used to judge if self.crt_user has right to access self.instance
        """
        if self.nolimit:
            return True
        if self.instance.pk ==None:
            if self.permit.can_add():
                return True
            #else:
                #return False

        return self.permit.can_access()
        # perm = self.instance._meta.app_label+'.change_'+self.instance._meta.model_name
        # return self.crt_user.has_perm(perm)
    

    
    def get_readonly_fields(self):
        ls=self.permit.readonly_fields()
        ls.extend(self.readonly)
        return ls
        # return []
    
    def get_row(self):
        """
        convert self.instance to dict.
        Note:Only convert Meta.fields ,not All fields
        """
        if not self.can_access():
            raise PermissionDenied('you have no Permission access %s'%self.instance._meta.model_name)

        # self.fields 是经过 权限 处理了的。可读写的字段
        
        # 由于现在的modelfields默认是select_for_update读取的instance，这个是加了锁的，不存在其他程序会修改数据。
        # 所以没有必要再刷新一次数据。
        # 但是考虑到可能会在内存中修改instance的字段值，可能会影响导出，所以还是决定刷新一下数据库。
        if self.instance.pk: 
            self.instance.refresh_from_db()
            
            
        if self.simple_dict:
            row = sim_dict(self.instance,include=self.fields.keys(),include_pk=True)
            row.update( self.dict_row(self.instance) )
        else:
            row = to_dict(self.instance,include=self.fields.keys())
            row.update( self.dict_row(self.instance) )
            
            ls=[]
            ls.extend(self.permit.readable_fields())
            ls.extend(self.permit.changeable_fields())
            
            for field in self.instance._meta.get_fields():
                if isinstance(field,(models.AutoField,models.BigAutoField)):
                    if field.name in ls and ( not self._meta.exclude or field.name not in self._meta.exclude) and\
                       field.name not in row:
                        row[field.name]=getattr(self.instance,field.name)
            row['_director_name']=self.get_director_name()
            row['meta_org_dict'] = self.get_org_dict(row)
        
        # 增加桥接
        for bridge,bridge_inst in zip(self.foreign_bridge,self.foreign_bridge_inst):
            #row.update( bridge.getRow(bridge_inst) )
            bridge.joinRow(bridge_inst,row)
            #if bridge.field_name in row:
                #del row[bridge.field_name]
            #if f'_{bridge.field_name}_label' in row:
                #del row[f'_{bridge.field_name}_label']
            #if f'_{bridge.field_name}_model' in row:
                #del row[f'_{bridge.field_name}_model']  
            
        return row

    def dict_row(self,inst):
        return {}
    
    def dict_head(self,head):
        return head      
    
    def clean_create(self):
        pass
    
    def save_form(self):
        """
        call by model render engin
        """
        
        if not (self.nolimit or self.crt_user.is_superuser):

            if not self.can_access():
                raise PermissionDenied('you have no Permission access %s'%self.instance._meta.model_name  )
        if self.forbid_change:
            raise PermissionDenied("%s is readonly"%self.instance._meta.model_name)
        
        for data in self.changed_data:
            if data in self.get_readonly_fields():
                raise PermissionDenied(" {data} is readonly".format(data=data))
        
        # 增加桥接
        for bridge,bridge_inst in zip(self.foreign_bridge,self.foreign_bridge_inst):
            bridge.saveForm(bridge_inst,base_inst = self.instance)     
        
        op=None
        if self.changed_data:
            op='change'
            detail=','.join(self.changed_data)
        
        #with transaction.atomic():
        #extra_log = self.clean_save()
        if self.instance.pk is None:
            op='add'
            detail=''
            if not self.allow_create:
                raise PermissionDenied('can not create!')
            self.clean_create()
            # 2020/07/30 屏蔽这里 后面直接就是保存
            # 2020/08/06  开启，该行不能屏蔽，因为manytomany 必须先保存才能生成 relation对象
            self.instance.save() # if instance is a new row , need save first then manytomany_relationship can create 
            
        # 2020/07/30 屏蔽这里，原因是其把clean_save里面修改的值给还原了
        # [2020/08/06] 开启，因为manytomany 需要 这样处理一下，才能 赋值 
        for k in self.changed_data:
            ## 测试时看到self.instance已经赋值了，下面这行代码可能没用,但是需要考虑下新建时 manytomany foreignkey 这些情况
            if k in self.kw:  # 排除开那些前端没有传递，而是后端model 默认生成的值
                              # 这些默认的值不能用 cleaned_data.get 来获取，因为他们是空
                # 2021/4/30 根据 [2020/08/06] 说明,现在改为只针对manytomany字段进行处理。
                # TODO 遇到manytomany时，测试一下是否必须要重新复制一次。
                if self.instance._meta.get_field(k).__class__ in [models.ManyToManyField]:
                    setattr(self.instance,k, self.cleaned_data.get(k) )
       
        # 过滤用户数据，与filterByUser类似 [2023/11/7]
        if getattr(self.instance,'cleanSaveByUser',None):
            self.instance.cleanSaveByUser(self.crt_user)
            
        # 2020/08/06 从571行挪到这里，以免 last row 代码覆盖了 clean_save的修改
        # 在clean_save 中 不能使用 pk==None来判断是否为创建row，应该使用self.is_create==Ture 来判断
        extra_log = self.clean_save()
        self.instance.save()
        if op or extra_log or self.extra_log:
            after_changed_data = sim_dict(self.instance, include= self.changed_data,include_pk=False,)
            dc = {
                'model': model_to_name(self.instance),
                'pk': self.instance.pk,
                'kind': op or 'extra_log',
                'user': self.crt_user.username if self.crt_user.is_authenticated else 'anonymous',
                '_before': self.before_changed_data,
                '_after': after_changed_data,
                '_label':{x: str( self.fields.get(x).label) for x in self.changed_data},
                'extral_log':self.extra_log
            }
            if extra_log:
                dc.update(extra_log)
            if self.op_log:
                dc.update(self.op_log)
            #sql_log.info(json.dumps(dc,cls=DirectorEncoder)) 
            modelfields_log.info(json.dumps(dc,cls=DirectorEncoder,ensure_ascii=False))
        self.after_save()
        return self.instance
    
    def clean_save(self): 
        return {}
    
    def after_save(self):
        pass
    
    def del_form(self):
        
        # 增加桥接   删除面积太大，展示屏蔽，[TODO] 应该是那种必须删除的才能删除
        #for bridge,bridge_inst in zip(self.foreign_bridge,self.foreign_bridge_inst):
            #bridge.delForm(bridge_inst,base_inst = self.instance)  
            
        if self.permit.can_del() and self.instance.pk:
            before_del_data = sim_dict(self.instance)
            
            model = model_to_name(self.instance)
            pk = self.instance.pk
            ex_del_log = self.ex_del_form()
            self.instance.delete()
            dc = {
                'model':model, 
                'pk':pk, 
                'kind':'delete', 
                'user': self.crt_user.username if self.crt_user.is_authenticated else 'anonymous',
                '_before':before_del_data,                 
            }
            if ex_del_log:
                dc.update(ex_del_log)
            modelfields_log.info(json.dumps(dc, cls=DirectorEncoder))
        else:
            raise PermissionDenied('No permission to delete %s'%str(self.instance))

    def ex_del_form(self): 
        return {}
    
    def save_log(self, dc): 
        modelfields_log.info(json.dumps(dc, cls=DirectorEncoder,ensure_ascii=False))
    
    def get_pop_edit_ctx(self,getrow='{pk:scope.vc.par_row.pk}',):
        ctx = self.get_head_context()
        ctx.update({
            'init_express':'ex.director_call("%(director_name)s",%(getrow)s).then(row=>{ex.vueAssign(scope.vc.row,row)})'%{'director_name':self.get_director_name(),'getrow':getrow},
            'ops_loc':'bottom',
            'action':'''var fctx=scope.head.fields_ctx;fctx.par_row=scope.row;cfg.pop_vue_com("com-form-one",scope.head.fields_ctx)''' 
        })
        return ctx

         
    

class Fields(ModelFields):
    """
    普通的form表单，与model层剥离开的
    """
    submit_to_backend = True  # 现在暂时放在Fields类中，后面考虑挪到ModelFields 中去
    def __init__(self, dc={}, pk=None, crt_user=None, nolimit=False, *args,select_for_update=True, **kw): 
        dc=self.clean_dict(dc) 
        self.kw=dc.copy()
        self.kw.update(kw)
        if pk is not None:
            self.kw['pk'] = pk
        if not crt_user:
            self.crt_user = get_request_cache()['request'].user
        else:
            self.crt_user = crt_user  
        self._errors={
        }
        # 太复杂，暂时不要权限
        self.nolimit = True

    
    def add_error(self,key,msg):
        if key not in self._errors:
            self._errors[key]=[]
        self._errors[key].append(msg)
    
    def get_errors(self):
        return self._errors
    
    def clean(self):
        if self.kw.get('meta_org_dict'):
            crt_mark_dc = self.get_org_dict()
            if crt_mark_dc:
                dif_dc = dif_mark_dict(crt_mark_dc, self.kw.get('meta_org_dict'))
            else:
                dif_dc ={}
            if dif_dc:
                heads = self.get_heads()
                head_names =[]
                for head in heads:
                    if head['name'] in dif_dc:
                        head_names.append(head['label'])
                        
                raise OutDateException('%s已经发生了变化,请确认后再进行操作!'%';'.join(head_names) )
            
    def is_valid(self):
        self.clean()
        if self._errors:
            return False
        else:
            return True
    
    def save_form(self): 
        "overwrite this method"
        print('here')
    
    def get_org_dict(self,row=None):
        if not row:
            # fields 的数据获取来自于非db orm类型。如果需要过期检查，需要定制该函数，手动去获取该行数据。
            return {}
            #row= self.dict_row()
        return make_mark_dict(row)
    
    def clean_dict(self, dc): 
        return dc
    
    def get_operations(self):
        ls=[]
        if self.submit_to_backend:
            ls.append({
                'name':'save',
                'editor':'com-btn',
                'label':_('保存'),
                'type':'primary',
                'icon':'el-icon-receiving',
                'click_express':'scope.ps.vc.submit()',
                'show_express':'rt= ! scope.vc.ctx.readonly_all'
                #'editor':'com-field-op-btn',
                #'label':'保存', 
                #'icon': 'fa-save',
                #'class':'btn btn-info'
            })
        else:
            ls.append({
                'name':'save',
                'editor':'com-btn',
                'label':'确定',
                'type':'primary',
                'icon':'el-icon-receiving',
                'show_express':'rt= ! scope.vc.ctx.readonly_all',
                'click_express':'scope.ps.vc.beforeSubmit().then(()=>{  if(scope.ps.vc.isValid()){ scope.ps.vc.$emit("finish",scope.ps.vc.row)}  })',
                    })
        return ls 
    
    def dict_row(self):
        return {
            #'_director_name':self.get_director_name()
        }
    
    def get_row(self): 
        row= self.dict_row()
        row.update( {
            '_director_name': self.get_director_name(),
            'meta_org_dict':self.get_org_dict(row),
        })
        return row

class FieldsSet(object):
    template=''
    def __init__(self,pk=None,crt_user=None):
        self.pk=pk
        self.crt_user=crt_user
    
    def get_context(self):
        return {}
        


        