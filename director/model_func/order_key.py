from helpers.director.kv import get_value,set_value
from django.utils import timezone

def date_order(key,digit=6):
    # 20190101xxxxxx
    datestr = timezone.now().strftime('%Y%m%d')
    crt_value = get_value(key,datestr+'0'*digit)
    if crt_value[:8] == datestr:
        point = int( crt_value[8:] )
        crt_point = point +1
    else:
        crt_point =0
    
    pointstr ='%%0%sd'%digit
    rt = datestr + pointstr%crt_point
    set_value(key, rt)
    return rt
