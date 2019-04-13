# encoding:utf-8
from __future__ import unicode_literals
from django import forms
from ..model_func.dictfy import form_to_head,to_dict, sim_dict,delete_related_query,model_to_name,from_dict,name_to_model,field_map
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
from ..models import LogModel
from helpers.director.base_data import director
from helpers.director.data_format.json_format import DirectorEncoder
from django.conf import settings
from django.utils.translation import ugettext as _
from helpers.director.middleware.request_cache import get_request_cache,request_cache
from helpers.func.collection.container import evalue_container
from django.db import transaction
import logging
from helpers.director.decorator import get_request_cache
# sql_log 可能没有什么用
#sql_log = logging.getLogger('director.sql_op')

modelfields_log = logging.getLogger('ModelFields.save_form')


class ModelFields(forms.ModelForm):
    """
    __init__函数，参数组合
    1. pk,crt_user 编辑，读取的时候
    2. instance,crt_user 编辑，读取的时候
    3. dc,crt_user 保存修改的时候。dc是新值组成的字典
    4. crt_user 新建的时候
    
    """
    readonly=[]
    field_sort=[]
    extra_mixins=[]
    hide_fields = []
    show_pk=False
    @classmethod
    def parse_request(cls,request):
        """
        传入参数的形式：
        row_search: key=value&..
        row_sort: _sort=key1,-key2
        page: _page=1
        row_filter:key=value&..
        """
        dc=request.GET.dict()
        pk=dc.pop('pk',None)
        return cls(pk=pk,crt_user=request.user,**dc) 
    
    def __init__(self,dc={},pk=None,crt_user=None,nolimit=False,*args,**kw):
        """
        调用情况：
        1. ajax save 时
        2. ajax get 时，获取数据，或者获取一个新的row数据。
        
        @dc: 当post save时 ,dc是前端传来的row字典
             当get 时，dc是前端传来的url参数，排除pk后的额外的字典
        """
        self.kw = kw.copy()
        
        if not crt_user:
            #self.crt_user=dc.get('crt_user')
            self.crt_user = get_request_cache()['request'].user
        else:
            self.crt_user = crt_user
            
        dc = self._clean_dict(dc)
        dc=self.clean_dict(dc)
        # if pk is None:
        if dc.get('pk') != None:
            pk=dc.get('pk')
        form_kw={}
        if 'instance' not in kw:
            if pk=='-1':  # -1 表示 最后一个记录 （一般用不到）
                form_kw['instance']=self._meta.model.objects.last()
            elif pk != None:  # 很多时候，pk=0 是已经创建了
                try:
                    form_kw['instance']= self._meta.model.objects.get(pk=pk)
                except self._meta.model.DoseNotExist:
                    raise Http404('Id that you request is not exist')
            else:
                form_kw['instance'] = self._meta.model()
        else:
            form_kw['instance']=kw.pop('instance')
        
        for k in dict(dc):
            # 强制 readonly的字段，不能修改
            inst =  form_kw['instance']
            if k in self.readonly:
                if hasattr(inst, "%s_id" % k):  # 如果是ForeignKey，必须要pk值才能通过 form验证
                    fieldcls = inst.__class__._meta.get_field(k)
                    if isinstance(fieldcls, models.ForeignKey):
                        dc[k] = getattr(inst, "%s_id" % k)
                        continue
                dc[k] =  getattr(form_kw['instance'] , k)  
        
        self.nolimit = nolimit
        self.kw.update(dc)

        super(ModelFields,self).__init__(dc,*args,**form_kw)
        self.custom_permit()
        
        self.pop_fields()
        self.init_value()
        
        self.op_log={}
        
        # 有事直接利用table的rows，而table进行了一定的修改显示，这些字段都是readonly的，所以要过滤掉这些字段，否则会造成严重后果。
        #self.changed_data = [x for x in self.changed_data if x not in self.readonly]
        # 保留下instance的原始值
        self.before_changed_data = sim_dict(self.instance, include= self.changed_data)
        
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
                        if hasattr(mapper_cls,'clean_field'):
                            dc[k] =  mapper_cls().clean_field(dc,k)
                        
                field_path = model_name+'.'+k
                if field_map.get(field_path):
                    map_cls = field_map[field_path]
                    field = model._meta.get_fields()
                    dc[k]=map_cls().clean_field(dc,k) 
        return dc
    
    def clean_dict(self,dc):   
        return dc
    
    def is_valid(self): 
        rt = super().is_valid()
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
        return {
            'heads':self.get_heads(),
            'row': self.get_row(),
            #'permit':self.get_permit(),
            'director_name':self.get_director_name(),
            'ops':self.get_operations(),
            'extra_mixins':self.extra_mixins
        } 
    
    @request_cache
    def get_head_context(self):
        heads = self.get_heads()
        ops =  self.get_operations()
        return {
            'heads':heads,
            'ops':ops,
            'director_name':self.get_director_name(),
            #'model_name':model_to_name(self._meta.model),
            'extra_mixins':self.extra_mixins
        }         
    
    def get_del_info(self):
        return {'%(model)s:%(inst)s <id=%(pk)s>'%{'model':self.instance.__class__.__name__,'inst':str(self.instance),'pk':self.instance.pk}:delete_related_query(self.instance)}
    
    def get_operations(self):
        ls=[]
        if self.permit.changeable_fields():
            ls.append({
                'name':'save','editor':'com-field-op-btn','label':'保存', 'icon': 'fa-save',
                'class':'btn btn-info btn-sm',
            })
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
        for k,v in self.fields.items():
            #if isinstance(include,(tuple,list)) and k not in include:
                #continue
            if k in self.hide_fields:
                continue
            
            dc = {'name':k,'label':str(v.label),
                  'help_text':str(v.help_text),
                  'editor':'linetext'}
                  
            if hasattr(v,'required'):
                dc['required'] = v.required   
                     
            if hasattr(v,'widget') and isinstance(v.widget,forms.widgets.Select):
                dc['editor'] = 'sim_select' 
                #dc['options']=[{'value':val,'label':str(lab)} for val,lab in v.widget.choices]
            elif v.__class__==forms.fields.CharField:
                if v.max_length:
                    dc.update({'editor':'linetext','maxlength':v.max_length})
                else:
                    dc.update({'editor':'blocktext'})
            elif v.__class__==forms.fields.BooleanField:
                dc['editor']='bool'
                #dc['no_auto_label']=True
            elif v.__class__ in [forms.fields.IntegerField,forms.fields.FloatField]:
                dc['editor']='number'
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
                
            dc = self.dict_head(dc)
            
            #if hasattr(v, 'choices') and 'options' not in dc :
                #options_name = '%(fieldName)s.options'% {'fieldName':fieldName}
                #catch = get_request_cache()
                #if not catch.get(options_name):
                    #catch[options_name]=[{'value':val,'label':str(lab)} for val,lab in v.choices]                
                #dc['options'] = catch[options_name]
            
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
        
        self.heads = heads
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
            
        heads=evalue_container(heads)
        for head in heads:
            if head['name']=='_meta_head':
                heads.remove(head)
                heads= [head]+heads
                break
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
        row = to_dict(self.instance,filt_attr=self.dict_row,include=self.fields)
        
        ls=[]
        ls.extend(self.permit.readable_fields())
        ls.extend(self.permit.changeable_fields())
        
        for field in self.instance._meta.get_fields():
            if isinstance(field,(models.AutoField,models.BigAutoField)):
                if field.name in ls and ( not self._meta.exclude or field.name not in self._meta.exclude) and\
                   field.name not in row:
                    row[field.name]=getattr(self.instance,field.name)
        row['_director_name']=self.get_director_name()
        return row

    def dict_row(self,inst):
        return {}
    
    
    def dict_head(self,head):
        return head      
    
    def save_form(self):
        """
        call by model render engin
        """
        
        if not (self.nolimit or self.crt_user.is_superuser):

            if not self.can_access():
                raise PermissionDenied('you have no Permission access %s'%self.instance._meta.model_name  )
 
            for data in self.changed_data:
                if data in self.get_readonly_fields():
                    raise PermissionDenied("Can't change {data}".format(data=data))
        
        op=None
        if self.changed_data:
            op='change'
            detail=','.join(self.changed_data)
        
        with transaction.atomic():
            if self.instance.pk is None:
                op='add'
                detail=''
                self.instance.save() # if instance is a new row , need save first then manytomany_relationship can create   
            for k in self.changed_data:
                ## 测试时看到self.instance已经赋值了，下面这行代码可能没用,但是需要考虑下新建时 manytomany foreignkey 这些情况
                setattr(self.instance,k, self.cleaned_data.get(k) )
            extra_log = self.clean_save()
            self.instance.save()
            
        if op or extra_log:
            after_changed_data = sim_dict(self.instance, include= self.changed_data)
            dc = {
                'model': model_to_name(self.instance),
                'pk': self.instance.pk,
                'kind': op or 'extra_log',
                'user': self.crt_user.username if self.crt_user.is_authenticated else 'anonymous',
                'before': self.before_changed_data,
                'after': after_changed_data,
            }
            if extra_log:
                dc.update(extra_log)
            if self.op_log:
                dc.update(self.op_log)
            #sql_log.info(json.dumps(dc,cls=DirectorEncoder)) 
            modelfields_log.info(json.dumps(dc,cls=DirectorEncoder))
        self.after_save()
        return self.instance
    
    def clean_save(self): 
        return {}
    
    def after_save(self):
        pass
    
    def del_form(self):
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
                'before':before_del_data,                 
            }
            if ex_del_log:
                dc.update(ex_del_log)
            modelfields_log.info(json.dumps(dc, cls=DirectorEncoder))
        else:
            raise PermissionDenied('No permission to delete %s'%str(self.instance))

    def ex_del_form(self): 
        return {}
    
    def save_log(self, dc): 
        modelfields_log.info(json.dumps(dc, cls=DirectorEncoder))
    

class Fields(ModelFields):
    """
    普通的form表单，与model层剥离开的
    """
    def __init__(self, dc={}, pk=None, crt_user=None, nolimit=False, *args, **kw): 
        self.kw=dc.copy()
        self.kw.update(kw)
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
        pass
    def is_valid(self):
        self.clean()
        if self._errors:
            return False
        else:
            return True
    
    def save_form(self): 
        "overwrite this method"
        print('here')
    
    
    def clean_dict(self, dc): 
        return dc
    
    def get_operations(self):
        ls=[]
        ls.append({
            'name':'save','editor':'com-field-op-btn','label':'保存', 'icon': 'fa-save','class':'btn btn-info'
        })
        return ls 
    def get_row(self): 
        return {
            '_director_name': self.get_director_name(),
        }

class FieldsSet(object):
    template=''
    def __init__(self,pk=None,crt_user=None):
        self.pk=pk
        self.crt_user=crt_user
    
    def get_context(self):
        return {}
        


        