# -*- encoding:utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.apps import apps
from django import forms
import json
from django.utils.timezone import localtime
from datetime import datetime
from django.utils.translation import ugettext as _
from ..pyenv import u
from .model_admin.base import model_dc
from django.core.exceptions import ValidationError
#from django.db.models.fields import related_descriptors

def get_or_none(model, **kw):
    """
    """
    try:
        obj = model.objects.filter(**kw).order_by('-id')[0]
        return obj
    except IndexError:
        return None

def model_to_name(model):
    """
    @model: model or instance
    """
    return model._meta.app_label+'.'+model._meta.model_name

def name_to_model(app_model_string):
    return apps.get_model(app_model_string)
    

def to_dict(instance,filt_attr=None,include=None,exclude=None,form=False):
    if form:
        form_cls=model_dc.get(instance.__class__).get('fields')
        form_obj = form_cls(instance=instance,nolimit=True)
        return form_obj.get_row()
    
    out=sim_dict(instance,filt_attr,include,exclude)
    out['pk']=instance.pk
    out['_class']= instance._meta.app_label+'.'+instance._meta.model_name
    if '_label' not in out.keys():
        out['_label']=unicode(instance)
    return out


def sim_dict(instance,filt_attr=None,include=None,exclude=None):
    """
    fields=['name','age'] 虽然中函数中fields是django中的model.field对象，但是这里为了方便，接受外部
                         输入是字段的名字
                         
    filt_attr(instance)是可调用对象，返回一个字典，包含已经处理过的属性。这些属性不会再被to_jd操作。
         或者直接是dict
    
    注意，返回的字典，是可以json化的才行。
    """
    fields=instance._meta.get_fields() # 如果用  instance._meta.fields 没有 manytomany (测试过) ,可能也没有 onetoone
    fields=[field for field in fields if isinstance(field,models.Field)]
    if include:
        fields=filter(lambda field:field.name in include,fields)
    if exclude:
        fields=filter(lambda field:field.name not in exclude,fields)
    if filt_attr:
        if callable(filt_attr):
            out=filt_attr(instance)
        else:
            out=filt_attr
    else:
        out={}
    for field in fields:
        if field.name in out: # or\
           #isinstance(field,(models.ManyToManyRel,models.ManyToOneRel)):
            continue
        else:
            proxy_cls = field_map.get(field.__class__)
            if proxy_cls:
                out[field.name] = proxy_cls().to_dict(instance,field.name)
                if isinstance(out[field.name],list):
                    # 如果遇到 manytomany的情况，是一个list
                    out['_%s_label'%field.name]=[unicode(x) for x in out[field.name]]
                else:
                    out['_%s_label'%field.name]=unicode(getattr(instance,field.name,''))
            else:
                
                # 考虑到使用到get_prep_value转换为str的field很少（大部分特殊的都在field_map类集中处理了。）
                # 所以修改为直接读取属性，而不是使用get_prep_value转换，因为jsonfield需要直接输出python对象。
                out[field.name]=getattr(instance,field.name,None) #field.get_prep_value( getattr(instance,field.name,None) )  
                if field.choices:
                    org_value= out[field.name]
                    mt = [x for x in field.choices if x[0]==org_value]
                    if mt:
                        out['_tr_'+field.name]=mt[0][1]
    if instance.id:
        out['id']=instance.id
    return out
    

class DatetimeProc(object):
    def to_dict(self,inst,name):
        value = getattr(inst,name,None)
        if value:
            return localtime(value).strftime('%Y-%m-%d %H:%M:%S')
        else:
            return ''
    
    def from_dict(self,value,field):
        """
        该函数需要check
        """
        return datetime.strptime(value,'%Y-%m-%d %H:%M:%S')
        
class ForeignProc(object):
    def to_dict(self,inst,name):
        foreign=getattr(inst,name,None)
        if foreign:
            return foreign.pk
        
    def from_dict(self,value,field):
        if isinstance(value,models.Model):
            return value
        else:
            model=field.rel.to
            if not value:
                return None
            else:
                return model.objects.get(pk=value)

class ManyProc(object):
    def to_dict(self,inst,name):
        if not inst.pk:
            return []
        else:
            out =[]
            for item in getattr(getattr(inst,name),'all')():
                out.append(item.pk)
            return out
    
    def from_dict(self,value,field):
        """
        TODO  think about : many_set
        """
        return value

class OneProc(object):
    def to_dict(self,inst,name):
        foreign=getattr(inst,name,None)
        if foreign:
            return foreign.pk 
    def from_dict(self,value,field):
        """may need test"""
        if isinstance(value,models.Model):
            return value
        else:
            model=field.rel.to
            return model.objects.get(pk=value)    

#from helpers.base.jsonfield import JsonField
#class JsonProc(object):
    #def to_dict(self,inst,name):
        #return getattr(inst,name)
    #def from_dict(self,)

class DateProc(object):
    def to_dict(self,inst,name):
        date=getattr(inst,name)
        if date:
            return date.isoformat()
        else:
            return ""
    def from_dict(self,value,field):
        """may need test"""
        return value     

field_map={
    models.DateTimeField:DatetimeProc,
    models.ForeignKey : ForeignProc,
    models.ManyToManyField:ManyProc,
    models.OneToOneField:OneProc,
    models.DateField:DateProc,
}

def from_dict(dc,model=None,pre_proc=None):
    """

    1. 半自动：
    processed_attr=pre_proc(dc,model) ; 返回处理过的字典processed，该processed用于剔除传入的dc参数
    
    """
    processed={}
    if model is None and '_class' in dc:
        model=apps.get_model(dc['_class'])
    if not model:
        raise UserWarning,'when constuct model object, but no model set'
    if pre_proc:
        processed=pre_proc(dc,model)
    for k in processed:
        dc.pop(k)         # 去除被pre_proc处理过的值， (因为处理过的值，不应再被 _convert_foreign处理)
        
    fields = model._meta.get_fields()
    for field in fields:
        value= dc.get(field.name,'__not_output')
        if value!='__not_output':
            if not value is None:
                if field_map.get(field.__class__):
                    processed[field.name] = field_map.get(field.__class__)().from_dict(value,field) 
                else:
                    # 由于有jsonfield这样的字段，不进行unicode处理，直接赋值python对象
                    #processed[field.name]=u(value)
                    processed[field.name]=value
            else:
                processed[field.name]=None

            
     #       
    # fpk_to_fobj(dc,model)
    # dc.update(processed)   # 把pre_proc的值合并回去 ，(因为下面要给 instance赋值)
    pk=dc.get('pk')
    if pk:
        instance=model.objects.get(pk=pk) 
        for k,v in processed.items():
            setattr(instance,k,v)                  
    else:
        # instance=model.objects.create(**processed)
        instance=model(**processed)
        #instance=model.objects.create()
        
    #for k,v in processed.items():
        #setattr(instance,k,v)     
    return instance
     

def get_model_label(ins_or_model):
    return '%s.%s'%(ins_or_model._meta.app_label,ins_or_model._meta.model_name)

def form_to_head(form,include=None):
    """
    convert form to head dict.一般接下来，会json.dumps()处理一下，然后传到到前端页面
    """
    out = []
    for k,v in form.fields.items():
        if isinstance(include,(tuple,list)) and k not in include:
            continue
        dc = {'name':k,'label':_(v.label),
              'required':v.required,
              'help_text':unicode(v.help_text),
              'type':'linetext'}
        
        if isinstance(v.widget,forms.widgets.Select):
            dc['type'] = 'sim_select' 
            dc['options']=[{'value':val,'label':lab} for val,lab in v.widget.choices]
        elif v.__class__==forms.fields.CharField:
            if v.max_length:
                dc.update({'type':'linetext','maxlength':v.max_length})
            else:
                dc.update({'type':'blocktext'})
        elif v.__class__==forms.fields.BooleanField:
            dc['type']='bool'
            #dc['no_auto_label']=True
        elif v.__class__ in [forms.fields.IntegerField,forms.fields.FloatField]:
            dc['type']='number'
        if v.__class__ ==forms.models.ModelMultipleChoiceField and \
            isinstance(v.widget,forms.widgets.SelectMultiple):
            dc['type']='tow_col'
        # elif v.__class__==forms.models.ModelChoiceField and \
        
        out.append(dc)
    return out

ID_tr=_('ID')

def model_to_head(model,include=[],exclude=[]):
    out = []
    for field in model._meta.get_fields():
        if isinstance(field,models.Field):
            #if isinstance(field._verbose_name, (str,unicode)):
                #dc = {'name':field.name,'label':_(field._verbose_name),}
            #else:
            dc= {'name':field.name,'label':_(field.verbose_name)}
            out.append(dc)
    if include:
        out=[x for x in out if x.get('name') in include]
        out.sort(key=lambda x : include.index(x.get('name')))
    else:
        out=[x for x in out if x.get('name') not in exclude]
    return out

# def save_model(row,scope):
    # if '_form' in row:
        # form = scope.get(row.get('_form'))
    # else:
        # model=apps.get_model(row['_class'])
        # for k,v in scope.items():
            # if isinstance(v,type) and issubclass(v,forms.ModelForm):
                # if hasattr(v,'Meta') and v.Meta.model==model:
                    # form = v
                    # break
    # return model_form_save(form,row)


# def model_form_save(form,models,success=None,**kw):
    # """
    # 保存 ModelForm。这个函数不如save_model智能。需要手动传入form。如果前端页面有_class信息，最好使用使用自动化的save_model函数
    
    # @form : 普通的django form
    # @models: dict: 代表是所有field的值
    
    # @success: callback(obj) : 
    # @kw : 可以传入user 等  /// 可以没有用处，等等调整它.
    
    # """
    # model_dict= models # kw.pop('models')
    # model_dict.update(kw)
    # model = form.Meta.model
    # pk=models.get('pk',None)
    # if pk:
        # inst = model.objects.get(pk=pk)
        # iform = form(model_dict,instance=inst)
    # else:
        # iform = form(model_dict)

    # if iform.is_valid():
        # model_dict.update(iform.cleaned_data)
        # obj = from_dict(model_dict,model)
        # if success:
            # return success(obj)
        # else:
            # obj.save()
            # return {'status':'success'}
    # else:
        # return {'errors':iform.errors}


def delete_related_query(inst):
    """
    When delet inst object,Django ORM will delet all related model instance.
    this function used to search related instance with inst,return string tree
    查询 删除inst时，所要删除的所有关联对象
    """
    if inst is None:
        return []  
    
    ls = []
    for rel in inst._meta.get_all_related_objects():
        if rel.on_delete.__name__=='CASCADE':
            name = rel.get_accessor_name()
            obj = getattr(inst,name,None)
            if obj is None:
                continue
            elif hasattr(obj,'all'):  # Foreign Key field
                for sub_obj in obj.all():
                    ls.append({'str':"{cls_name}:{content}".format(cls_name = sub_obj.__class__.__name__,content=unicode(sub_obj)),
                               'related':delete_related_query(sub_obj)})
            else:   # OneToOne related
                ls.append({'str':"{cls_name}:{content}".format(cls_name = obj.__class__.__name__,content=unicode(obj)),
                           'related':delete_related_query(obj)})   
                
    for rel in inst._meta.get_all_related_many_to_many_objects():  # ManyToMany Related
        name = rel.get_accessor_name()
        many_to_many_rels = getattr(inst,name)
        for obj in many_to_many_rels.all():
            ls.append({'str':'{obj_cls}({obj_content}) to {inst_cls}({inst_content}) relationship '.format(obj_cls=obj.__class__.__name__,\
                                obj_content=u(obj),inst_cls=inst.__class__.__name__,inst_content=unicode(obj)),
                       'related':[]})
    for field in inst._meta.get_fields():    # manyToMany Field
        if isinstance(field,models.ManyToManyField):
            name = field.name
            if not inst.pk: # instance must save before access manyToMany
                continue
            for obj in getattr(inst,name).all():
                ls.append({'str':'{obj_cls}({obj_content}) to {inst_cls}({inst_content}) relationship '.format(obj_cls=obj.__class__.__name__,\
                                obj_content=u(obj),inst_cls=inst.__class__.__name__,inst_content=unicode(obj)),
                       'related':[]})
    
    return ls
            
            

def AbstractClassWithoutFieldsNamed(bas_cls, *excl):
    """
    Removes unwanted fields from abstract base classes.

    Usage::
    >>> from oscar.apps.address.abstract_models import AbstractBillingAddress

    >>> from koe.meta import AbstractClassWithoutFieldsNamed as without
    >>> class BillingAddress(without(AbstractBillingAddress, 'phone_number')):
    ...     pass
    """
    if not bas_cls._meta.abstract:
        raise Exception("Not an abstract model")
        
    class cls(bas_cls):
        class Meta:
            abstract=True
            
    remove_fields = [f for f in cls._meta.local_fields if f.name in excl]
    for f in remove_fields:
        cls._meta.local_fields.remove(f)
    return cls
       
def permit_to_dict(user,inst):
    fields_cls = model_dc[inst.__class__]["fields"]
    fields_obj = fields_cls(instance=inst,crt_user=user)
    return fields_obj.get_row()

def permit_save_model(user,row,**kw):
    for k in row: # convert model instance to pk for normal validation
        if isinstance(row[k],models.Model):
            row[k]=row[k].pk
            
    model= name_to_model(row['_class'])
    fields_cls = model_dc.get(model).get('fields')

    fields_obj = fields_cls(row,crt_user=user,**kw)
    if fields_obj.is_valid():
        fields_obj.save_form()
        return fields_obj
    else:
        raise ValidationError(fields_obj.errors)


# for k in row: # convert model instance to pk for normal validation
    # if isinstance(row[k],models.Model):
        # row[k]=row[k].pk

# model= name_to_model(row['_class'])
# fields_cls = model_dc.get(model).get('fields')

# kw=request.GET.dict()
# fields_obj=fields_cls(row,crt_user=user,**kw)
# if fields_obj.is_valid():
    # fields_obj.save_form()
    # return fields_obj.get_row()
# else:
    # raise ValidationError(fields_obj.errors)



