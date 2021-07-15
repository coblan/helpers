from django.utils import timezone

def default_search_range_time(search_args,name, tm_delta):
    start_str = search_args.get('_start_%s'%name)
    end_str =  search_args.get('_end_%s'%name)
    if start_str:
        start = timezone.datetime.strptime(start_str,'%Y-%m-%d %H:%M:%S')
    else:
        start = None
    if end_str:
        end = timezone.datetime.strptime(end_str,'%Y-%m-%d %H:%M:%S')
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
    
    if start >= end:
        raise UserWarning('起始时间不能大于结束时间')
    search_args['_start_%s'%name] = start.strftime('%Y-%m-%d %H:%M:%S')
    search_args['_end_%s'%name] = end.strftime('%Y-%m-%d %H:%M:%S')
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
    
    if start >= end:
        raise UserWarning('起始时间不能大于结束时间')
    search_args['_start_%s'%name] = start.strftime('%Y-%m-%d')
    search_args['_end_%s'%name] = end.strftime('%Y-%m-%d')
    return start,end

    