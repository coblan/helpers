# encoding:utf-8
from __future__ import unicode_literals
from django.utils import timezone

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

