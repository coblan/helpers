# -*- encoding:utf-8 -*-
from __future__ import unicode_literals

from ..base_data import model_dc

import json
from django.db import models
from django.apps import apps
from django import forms
from django.utils.timezone import localtime,datetime
from django.utils.translation import ugettext as _
#from md5 import md5
from .field_proc import BaseFieldProc
from .hash_dict import hash_dict,make_mark_dict
from ..base_data import field_map

def get_choice_label(instance,field_name):
    field =  instance._meta.get_field(field_name)
    value = getattr(instance,field_name,None)
    dc = dict(field.choices)
    return dc.get(value)

def model_to_name(model):
    """
    @model: model or instance
    
    """
    return model._meta.app_label+'.'+model._meta.model_name

def name_to_model(app_model_string):
    return apps.get_model(app_model_string)
 
def field_label(model,key):
    field = model._meta.get_field(key)
    return field.verbose_name
    

def to_dict(instance,filt_attr=None,include=None,exclude=None,hash_keys=None,form=False,include_pk=True):
    if form:
        form_cls=model_dc.get(instance.__class__).get('fields')
        form_obj = form_cls(instance=instance,nolimit=True)
        return form_obj.get_row()
    
    out=sim_dict(instance,filt_attr,include,exclude,include_pk=include_pk)
    
    out['_class']= instance._meta.app_label+'.'+instance._meta.model_name
    if '_label' not in out.keys():
        out['_label']=str(instance)

    #fields_name = [x.name for x in instance._meta.get_fields()]
    #valide_name_list = [x for x in fields_name if x in out.keys()]
    #out['meta_hash_fields'] = ','.join(valide_name_list)
    #out['meta_org_dict'] = make_mark_dict(instance.__dict__,valide_name_list)
    return out

def model_fields_names(model_or_inst):
    fields=model_or_inst._meta.get_fields() # 如果用  instance._meta.fields 没有 manytomany (测试过) ,可能也没有 onetoone
    fields=[field for field in fields if isinstance(field,models.Field)]
    
    return [x.name for x in fields]

def sim_dict(instance,filt_attr=None,include=None,exclude=None,include_id=True,include_pk=True,label=True):
    """
    fields=['name','age'] 虽然中函数中fields是django中的model.field对象，但是这里为了方便，接受外部
                         输入是字段的名字
                         
    filt_attr(instance)是可调用对象，返回一个字典，包含已经处理过的属性。这些属性不会再被to_jd操作。
         或者直接是dict
    
    注意，返回的字典，是可以json化的才行。
    """
    model_path = instance._meta.app_label+'.'+instance._meta.model_name
    fields=instance._meta.get_fields() # 如果用  instance._meta.fields 没有 manytomany (测试过) ,可能也没有 onetoone
    fields=[field for field in fields if isinstance(field,models.Field)]
    if include != None :
        fields=filter(lambda field:field.name in include,fields)
    if exclude != None:
        fields=filter(lambda field:field.name not in exclude,fields)
    if filt_attr:
        if callable(filt_attr):
            has_dict=filt_attr(instance)
        else:
            has_dict=filt_attr
    else:
        has_dict={}
        
    out = dict(has_dict)
    for field in fields:
        if field.name in out: # or\
           #isinstance(field,(models.ManyToManyRel,models.ManyToOneRel)):
            continue
        else:
            mapper_cls=field_map.get('%s.%s'%(model_path,field.name))
            if not mapper_cls:
                mapper_cls = field_map.get(field.__class__)
                
            if mapper_cls:
                mapper = mapper_cls(instance=instance,name=field.name,model=field.model)
                out.update( mapper.to_dict(instance,field.name) )
                if '_%s_label'%field.name in out:
                    continue
                #if hasattr(mapper,'get_label'):
                    #out['_%s_label'%field.name]=mapper.get_label(instance,field.name)
                #if isinstance(out.get(field.name),list):
                    ## 如果遇到 manytomany的情况，是一个list
                if isinstance(field,models.ManyToManyField):
                    out['_%s_label'%field.name]=[str(x) for x in out[field.name]]
                
                # 下面生成 _{name}_label
                if '_%s_label'%field.name in out:
                    continue                
                elif field.choices:
                    org_value= out[field.name]
                    mt = [x for x in field.choices if x[0]==org_value]
                    if mt:
                        out[ '_%s_label'%field.name]=mt[0][1]
            else:
                
                # 考虑到使用到get_prep_value转换为str的field很少（大部分特殊的都在field_map类集中处理了。）
                # 所以修改为直接读取属性，而不是使用get_prep_value转换，因为jsonfield需要直接输出python对象。
                out[field.name]=getattr(instance,field.name,None) #field.get_prep_value( getattr(instance,field.name,None) )  
                if '_%s_label'%field.name in out:
                    continue                
                if field.choices:
                    org_value= out[field.name]
                    mt = [x for x in field.choices if x[0]==org_value]
                    if mt:
                        out[ '_%s_label'%field.name]=mt[0][1]
                        

    #if 'id' in [x.name for x in instance._meta.get_fields()] and \
       #instance.id:
        #out['id']=instance.id
    if include == None:
        # 2024/1/8 如果有include传入，那么就不单独处理id了。
        if include_id:
            if 'id' not in out and hasattr(instance,'id'):
                #out['id'] = instance.id
                out['id'] = clean_field_for_js(instance._meta.get_field('id'),instance)
        else:
            if 'id' in out:
                del out['id']            
        
    if  'pk' not in out and  include_pk:
        #out['pk']=instance.pk
        out['pk']= clean_field_for_js(instance._meta.pk,instance)
    if not label:
        ls = list( out.keys() )
        for k in ls:
            if k.startswith('_'):
                del out[k]
    
    return out
    

def clean_field_for_js(field,instance):
    """
    清理id或者pk的类型，因为有些字段前端不能正常显示，所以需要转换为字符串，例如bigint会产生溢出，后面几位数全部变成0。
    """
    model_path = instance._meta.app_label+'.'+instance._meta.model_name
    mapper_cls=field_map.get('%s.%s'%(model_path,field.name))
    if not mapper_cls:
        mapper_cls = field_map.get(field.__class__)
    if mapper_cls:
        mapper = mapper_cls(instance=instance,name=field.name,model=field.model)
        return mapper.to_dict(instance,field.name).get(field.name)
    else:
        return getattr(instance,field.name)

def from_dict(dc,model=None,pre_proc=None):
    """
    **该函数不应该再使用**
    
    1. 半自动：
    processed_attr=pre_proc(dc,model) ; 返回处理过的字典processed，该processed用于剔除传入的dc参数
    
    """
    processed={}
    if model is None and '_class' in dc:
        model=apps.get_model(dc['_class'])
    if not model:
        raise UserWarning('when constuct model object, but no model set')
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
                    processed[field.name] = field_map.get(field.__class__)().clean_field(dc,field.name) 
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
    这个函数功能挪到 modelfields 里面去了，这个函数应该是没有用了 [2018-8-1]
    convert form to head dict.一般接下来，会json.dumps()处理一下，然后传到到前端页面
    
    
    """
    out = []
    for k,v in form.fields.items():
        if isinstance(include,(tuple,list)) and k not in include:
            continue
        dc = {'name':k,'label':_(v.label),
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
            dc['editor']='com-field-number'
        elif v.__class__  == forms.fields.DateField:
            dc['editor']='date'
        if v.__class__ ==forms.models.ModelMultipleChoiceField and \
            isinstance(v.widget,forms.widgets.SelectMultiple):
            dc['editor']='field_multi_chosen'
            
        model_field = form._meta.model._meta.get_field(k)
        fieldName = model_to_name(form._meta.model) + '.' + k
        if fieldName in field_map:
            mapper=field_map[fieldName]
            mapper(form.instance).dict_field_head(dc)
        elif model_field.__class__ in field_map:
            mapper=field_map[model_field.__class__]
            mapper(form.instance).dict_field_head(dc)   
            
        out.append(dc)
    return out

# 为了将ID翻译成 序号
ID_tr= _('ID')

def model_to_head(model,include=[],exclude=[]):
    """不要再使用。被table 的 函数替换掉了"""
    out = []
    model_name = model_to_name(model)
    for field in model._meta.get_fields():
        if isinstance(field,models.Field):
            #if isinstance(field._verbose_name, (str,unicode)):
                #dc = {'name':field.name,'label':_(field._verbose_name),}
            #else:
            dc= {'name':field.name,'label':_(field.verbose_name)}
            fieldName = model_name + '.' + field.name
            if fieldName in field_map:
                mapper = field_map.get(fieldName)
                mapper(field = field).dict_table_head(dc)
            elif field.__class__ in field_map:
                mapper = field_map.get(field.__class__)
                if hasattr(mapper,'dict_table_head'):
                    mapper(field = field).dict_table_head(dc)
            elif isinstance(field,models.ForeignKey):
                dc['editor']='com-table-label-shower'            
                
            out.append(dc)
    if include:
        out=[x for x in out if x.get('name') in include]
        out.sort(key=lambda x : include.index(x.get('name')))
    else:
        out=[x for x in out if x.get('name') not in exclude]
    return out


def delete_related_query(inst,deep_level=0,include_relation=True,parents=None):
    """
    When delet inst object,Django ORM will delet all related model instance.
    this function used to search related instance with inst,return string tree
    查询 删除inst时，所要删除的所有关联对象
    @deep_level: 递归调用时，程序自动传入的当前level数。递归到4层时，就会退出。
    @parents=[]  root调用的时候需要弄一个parents=[],防止递归删除，deep_level占时无用了
    """
    if inst is None:
        return []  
    if inst.__class__ in parents:
        return []
    if deep_level>10:
        # 在del_form中，会检查是否有cascade_delete 删除，只需要递归一层即可，所以传入deep_level=9防止递归。
        return []
    parents.append(inst.__class__)
    
    ls = []
    all_related_objects =  [
        f for f in inst._meta.get_fields()
        if (f.one_to_many or f.one_to_one)
        and f.auto_created and not f.concrete
    ]
    all_related_many_to_many_objects =  [
        f for f in inst._meta.get_fields(include_hidden=True)
        if f.many_to_many and f.auto_created
    ]
    for rel in all_related_objects :   #inst._meta.get_all_related_objects(): django 1.10 has changed
        if rel.on_delete.__name__=='CASCADE':
            name = rel.get_accessor_name()
            obj = getattr(inst,name,None)
            if obj is None:
                continue
            elif hasattr(obj,'all'):  # Foreign Key field
                for sub_obj in obj.all():
                    if len(ls) >3:
                        ls.append({'str':'......'})
                        break                    
                    ls.append({'str':"{content}  ({cls_name})".format(cls_name = sub_obj.__class__.__name__,content=str(sub_obj)),
                               'related':delete_related_query(sub_obj,deep_level=deep_level+1,parents=parents)})
            else:   # OneToOne related
                if len(ls) >3:
                    ls.append({'str':'......',})
                    continue               
                ls.append({'str':"{content}  ({cls_name})".format(cls_name = obj.__class__.__name__,content=str(obj)),
                           'related':delete_related_query(obj,deep_level=deep_level+1,parents=parents)})   
                
    if include_relation:
        for rel in all_related_many_to_many_objects:  #inst._meta.get_all_related_many_to_many_objects():  # ManyToMany Related
            name = rel.get_accessor_name()
            many_to_many_rels = getattr(inst,name)
            for obj in many_to_many_rels.all():
                if len(ls)>4:
                    ls.append({'str':'......',})
                    break                
                ls.append({'str':'{obj_cls}({obj_content}) to {inst_cls}({inst_content}) relationship '.format(obj_cls=obj.__class__.__name__,\
                                    obj_content=str(obj),inst_cls=inst.__class__.__name__,inst_content=str(obj)),
                           'related':[]})
        for field in inst._meta.get_fields():    # manyToMany Field          
            if isinstance(field,models.ManyToManyField):
                name = field.name
                if not inst.pk: # instance must save before access manyToMany
                    continue
                for obj in getattr(inst,name).all():
                    if len(ls)>4:
                        ls.append({'str':'......',})
                        break                      
                    ls.append({'str':'{obj_cls}({obj_content}) to {inst_cls}({inst_content}) relationship '.format(obj_cls=obj.__class__.__name__,\
                                    obj_content=str(obj),inst_cls=inst.__class__.__name__,inst_content=str(obj)),
                           'related':[]})
    parents.pop()
    return ls
       
def permit_to_dict(user,inst):
    fields_cls = model_dc[inst.__class__]["fields"]
    fields_obj = fields_cls(instance=inst,crt_user=user)
    return fields_obj.get_row()





