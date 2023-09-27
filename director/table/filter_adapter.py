# encoding:utf-8
from __future__ import unicode_literals
from django.utils import timezone
from ..model_func.dictfy import model_to_name,field_map,BaseFieldProc

def datetime_range_adapter(search_args,name,month=None):
    """
    @name:字段名字
    @month:从今天往前推几个月
    """
    start_name = '_start_%s'%name
    end_name='_end_%s'%name
    show_dict={}
    #proc_dict={}
    if month is not None:
        today = timezone.now()
        sp = timezone.timedelta(days=30*month)
        last = today-sp
        def_start = last.strftime('%Y-%m-%d')
        def_end=today.strftime('%Y-%m-%d')
 
        show_dict[start_name]= search_args.get(start_name,def_start)
        show_dict[end_name] = search_args.get(end_name,def_end)
    
    if search_args.get(end_name):
        dd = timezone.datetime.strptime(search_args[end_name],'%Y-%m-%d') 
        sp_one_day = timezone.timedelta(days=1)
        real_end = dd+sp_one_day
        proc_dict[end_name] = real_end.strftime('%Y-%m-%d')
    return proc_dict,show_dict


def filter_head(model,field_name):
    """
    @model:数据库表
    @field_name:字段名
    
    返回：
    filter_head   {'name': 'kind', 'label': '单位类型', 'editor': 'com-filter-select', 'options': [{'value': 1, 'label': '重点监管单位'}, {'value': 2, 'label': '九小场所'}, {'value': 3, 'label': '其他单位'}, {'value': 4, 'label': '沿街商铺'}, {'value': 5, 'label': '居民小区'}]}

    """
    #model_name = model_to_name(model)
    #model_field_name = '%s.%s'%(model_name,field_name)
    #proc_cls =field_map.get(model_field_name, None)
    f = model._meta.get_field(field_name)
    proc_cls  =field_map.get(f.__class__)      
    
    if not proc_cls:
        proc_cls =  BaseFieldProc
    
    filter_head = proc_cls(name=field_name,model=model).filter_get_head(field_name,model)
    return filter_head  