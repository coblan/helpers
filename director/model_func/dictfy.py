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
from .hash_dict import hash_dict
from ..base_data import field_map



def model_to_name(model):
    """
    @model: model or instance
    
    """
    return model._meta.app_label+'.'+model._meta.model_name

def name_to_model(app_model_string):
    return apps.get_model(app_model_string)
    

def to_dict(instance,filt_attr=None,include=None,exclude=None,hash_keys=None,form=False):
    if form:
        form_cls=model_dc.get(instance.__class__).get('fields')
        form_obj = form_cls(instance=instance,nolimit=True)
        return form_obj.get_row()
    
    out=sim_dict(instance,filt_attr,include,exclude)
    out['pk']=instance.pk
    out['_class']= instance._meta.app_label+'.'+instance._meta.model_name
    if '_label' not in out.keys():
        out['_label']=str(instance)
    if '_hash' not in out.keys():
        out['_hash']=hash_dict(out,hash_keys)
        #out['_md5']=md5(out).hexdigest() 
    return out


def sim_dict(instance,filt_attr=None,include=None,exclude=None):
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
            mapper_cls=field_map.get('%s.%s'%(model_path,field.name))
            if not mapper_cls:
                mapper_cls = field_map.get(field.__class__)
                
            if mapper_cls:
                mapper = mapper_cls()
                out.update( mapper.to_dict(instance,field.name) )
                if '_%s_label'%field.name in out:
                    continue
                #if hasattr(mapper,'get_label'):
                    #out['_%s_label'%field.name]=mapper.get_label(instance,field.name)
                if isinstance(out.get(field.name),list):
                    # 如果遇到 manytomany的情况，是一个list
                    out['_%s_label'%field.name]=[str(x) for x in out[field.name]]
                else:
                    out['_%s_label'%field.name]=str(getattr(instance,field.name,''))
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
    return out
    

#class DatetimeProc(BaseFieldProc):
    #def to_dict(self,inst,name):
        #value = getattr(inst,name,None)
        #if value:
            #return {
                #name:value.strftime('%Y-%m-%d %H:%M:%S')
                #}
        #else:
            #return {}
        
    #def clean_field(self, dc, name):
        #if dc[name]:
            #return datetime.strptime(dc[name],'%Y-%m-%d %H:%M:%S')
        #else:
            #return dc[name]
    
    #def from_dict(self,value,field):
        #"""
        #该函数需要check
        #"""
        #return datetime.strptime(value,'%Y-%m-%d %H:%M:%S')
        
#class ForeignProc(BaseFieldProc):
    #def to_dict(self,inst,name):
        #foreign=getattr(inst,name,None)
        #if foreign:
            #return {
                #name:foreign.pk,
                #'_%s_model'%name:model_to_name(foreign.__class__),
                #'_%s_label'%name:unicode(foreign)
            #}
        #else:
            #return {}
    
    #def clean_field(self,dc,name):
        #model = name_to_model( dc.get('_%s_model'%name) )
        #return model.objects.get(pk=dc.get(name))     
    
    ##def get_label(self,inst,name):
        ##foreign=getattr(inst,name,None)
        ##if foreign:
            ##return unicode(foreign)
    
    ##def from_dict(self,value,field):
        ##if isinstance(value,models.Model):
            ##return value
        ##else:
            ##model=field.rel.to
            ##if not value:
                ##return None
            ##else:
                ##return model.objects.get(pk=value)

#class ManyProc(BaseFieldProc):
    #def to_dict(self,inst,name):
        #out =[]
        #if inst.pk:
            #for item in getattr(getattr(inst,name),'all')():
                #out.append(item.pk)
                
        #return {
            #name:out
            #}

    
    #def from_dict(self,value,field):
        #"""
        #TODO  think about : many_set
        #"""
        #return value

#class OneProc(BaseFieldProc):
    #def to_dict(self,inst,name):
        #foreign=getattr(inst,name,None)
        #if foreign:
            #return {
                #name: foreign.pk ,
                #'_%s_model'%name:model_to_name(foreign.__class__)
            #}
        #else:
            #return {}
    
    #def clean_field(self,dc,name):
        #model = name_to_model( dc.get('_%s_model'%name) )
        #return model.objects.get(pk=dc.get(name))  
 
    
    #def from_dict(self,value,field):
        #"""may need test"""
        #if isinstance(value,models.Model):
            #return value
        #else:
            #model=field.rel.to
            #return model.objects.get(pk=value)    

#from helpers.base.jsonfield import JsonField
#class JsonProc(object):
    #def to_dict(self,inst,name):
        #return getattr(inst,name)
    #def from_dict(self,)

#class DateProc(BaseFieldProc):
    #def to_dict(self,inst,name):
        #date=getattr(inst,name)
        #if date:
            #return {name:date.isoformat()}
        #else:
            #return {}
        
  

#class DecimalProc(BaseFieldProc):
    #def to_dict(self,inst,name):
        #data = getattr(inst,name)
        #return {name:unicode(data)}
    
    #def clean_field(self,dc,name):
        #return float(dc.get(name))

#class BoolProc(BaseFieldProc):
    #pass


#field_map.update({
    ##models.DateTimeField:DatetimeProc,
    ##models.ForeignKey : ForeignProc,
    ##models.ManyToManyField:ManyProc,
    ##models.OneToOneField:OneProc,
    ##models.DateField:DateProc,
    ##models.DecimalField:DecimalProc,
#})


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
            dc['options']=[{'value':val,'label':str(lab)} for val,lab in v.widget.choices]
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
            #dc['editor']='tow_col'
        # elif v.__class__==forms.models.ModelChoiceField and \
        
        model_field = form._meta.model._meta.get_field(k)
        if model_field.__class__ in field_map:
            mapper=field_map[model_field.__class__]
            if hasattr(mapper,'dict_field_head'):
                dc.update( mapper().dict_field_head(dc) )
        out.append(dc)
    return out

# 为了将ID翻译成 序号
ID_tr=_('ID')

def model_to_head(model,include=[],exclude=[]):
    out = []
    for field in model._meta.get_fields():
        if isinstance(field,models.Field):
            #if isinstance(field._verbose_name, (str,unicode)):
                #dc = {'name':field.name,'label':_(field._verbose_name),}
            #else:
            dc= {'name':field.name,'label':_(field.verbose_name)}
            if isinstance(field,models.ForeignKey):
                dc['editor']='com-table-label-shower'
            
            if field.__class__ in field_map:
                mapper = field_map.get(field.__class__)
                if hasattr(mapper,'dict_table_head'):
                    dc.update(mapper().dict_table_head(dc))
                
            out.append(dc)
    if include:
        out=[x for x in out if x.get('name') in include]
        out.sort(key=lambda x : include.index(x.get('name')))
    else:
        out=[x for x in out if x.get('name') not in exclude]
    return out


def delete_related_query(inst):
    """
    When delet inst object,Django ORM will delet all related model instance.
    this function used to search related instance with inst,return string tree
    查询 删除inst时，所要删除的所有关联对象
    """
    if inst is None:
        return []  
    
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
                    ls.append({'str':"{cls_name}:{content}".format(cls_name = sub_obj.__class__.__name__,content=str(sub_obj)),
                               'related':delete_related_query(sub_obj)})
            else:   # OneToOne related
                ls.append({'str':"{cls_name}:{content}".format(cls_name = obj.__class__.__name__,content=str(obj)),
                           'related':delete_related_query(obj)})   
                
    for rel in all_related_many_to_many_objects:  #inst._meta.get_all_related_many_to_many_objects():  # ManyToMany Related
        name = rel.get_accessor_name()
        many_to_many_rels = getattr(inst,name)
        for obj in many_to_many_rels.all():
            ls.append({'str':'{obj_cls}({obj_content}) to {inst_cls}({inst_content}) relationship '.format(obj_cls=obj.__class__.__name__,\
                                obj_content=str(obj),inst_cls=inst.__class__.__name__,inst_content=str(obj)),
                       'related':[]})
    for field in inst._meta.get_fields():    # manyToMany Field
        if isinstance(field,models.ManyToManyField):
            name = field.name
            if not inst.pk: # instance must save before access manyToMany
                continue
            for obj in getattr(inst,name).all():
                ls.append({'str':'{obj_cls}({obj_content}) to {inst_cls}({inst_content}) relationship '.format(obj_cls=obj.__class__.__name__,\
                                obj_content=str(obj),inst_cls=inst.__class__.__name__,inst_content=str(obj)),
                       'related':[]})
    
    return ls
       
def permit_to_dict(user,inst):
    fields_cls = model_dc[inst.__class__]["fields"]
    fields_obj = fields_cls(instance=inst,crt_user=user)
    return fields_obj.get_row()




