from django.utils import timezone


def default_search_range_time(search_args,name, tm_delta,second_only_promt = True):
    """
    如果没有日期，会输出默认日期
    """
    if second_only_promt:
        return check_search_range_time(search_args, name, tm_delta)
    start_str = search_args.get('_start_%s'%name)
    end_str =  search_args.get('_end_%s'%name)
    if start_str:
        if isinstance(start_str,str):
            start = timezone.datetime.strptime(start_str,'%Y-%m-%d %H:%M:%S')
        else:
            # 有可能在上游，start_str处理成了 datetime对象
            start = start_str
    else:
        start = None
    if end_str:
        if isinstance(end_str,str):
            end = timezone.datetime.strptime(end_str,'%Y-%m-%d %H:%M:%S')
        else:
            end = end_str
    else:
        end = None
        
    now = timezone.now()  
    if not start and not end:
        start = now - tm_delta
        end = now
    elif start and not end:
        end = start + tm_delta
    elif not start and end:
        start = end - tm_delta
    
    if start > end:
        raise UserWarning('起始时间不能大于结束时间')
    search_args['_start_%s'%name] = start.strftime('%Y-%m-%d %H:%M:%S')
    if not end_str and end != now:
        search_args['_end_%s'%name] = end.strftime('%Y-%m-%d %H:%M:%S')
    return start,end

def check_search_range_time(search_args,name, tm_delta):
    start_str = search_args.get('_start_%s'%name)
    end_str =  search_args.get('_end_%s'%name)
    if start_str:
        if isinstance(start_str,str):
            start = timezone.datetime.strptime(start_str,'%Y-%m-%d %H:%M:%S')
        else:
            # 有可能在上游，start_str处理成了 datetime对象
            start = start_str
    else:
        if '_not_first' in search_args:
            raise UserWarning('必须输入开始时间')
        start = None
    if end_str:
        if isinstance(end_str,str):
            end = timezone.datetime.strptime(end_str,'%Y-%m-%d %H:%M:%S')
        else:
            end = end_str
    else:
        end = None
        
    now = timezone.now()  
    if not start and not end:
        start = now - tm_delta
        end = now
    if not end:
        end = now
    #elif start and not end:
        #end = start + tm_delta
    #elif not start and end:
        #start = end - tm_delta
    
    if start > end:
        raise UserWarning('起始时间不能大于结束时间')
    if '_not_first' not in search_args:
        search_args['_start_%s'%name] = start.strftime('%Y-%m-%d %H:%M:%S')
    search_args['_not_first'] = 1
    #if not end_str and end != now:
        #search_args['_end_%s'%name] = end.strftime('%Y-%m-%d %H:%M:%S')
    return start,end



def default_search_range_date(search_args,name, tm_delta):
    """"""
    start_str = search_args.get('_start_%s'%name)
    end_str =  search_args.get('_end_%s'%name)
    if start_str:
        start = timezone.datetime.strptime(start_str,'%Y-%m-%d')
    else:
        start = None
    if end_str:
        end = timezone.datetime.strptime(end_str,'%Y-%m-%d')
    else:
        end = None
        
    if not start and not end:
        now = timezone.now()
        start = now - tm_delta
        end = now
    elif start and not end:
        end = start + tm_delta
    elif not start and end:
        start = end - tm_delta
    
    if start > end:
        raise UserWarning('起始时间不能大于结束时间')
    search_args['_start_%s'%name] = start.strftime('%Y-%m-%d')
    search_args['_end_%s'%name] = end.strftime('%Y-%m-%d')
    return start,end


def adapt_range_time(search_args,name):
    """
    start,end = adapt_range_time(search_args,'createtime')
    把时间补齐
    """
    start_str = search_args.get('_start_%s'%name)
    end_str =  search_args.get('_end_%s'%name)
    if start_str:
        if isinstance(start_str,str):
            start = timezone.datetime.strptime(start_str,'%Y-%m-%d %H:%M:%S')
        else:
            # 有可能在上游，start_str处理成了 datetime对象
            start = start_str
    else:
        start = None
    if end_str:
        if isinstance(end_str,str):
            end = timezone.datetime.strptime(end_str,'%Y-%m-%d %H:%M:%S')
        else:
            end = end_str
    else:
        end = timezone.now()
    return start,end