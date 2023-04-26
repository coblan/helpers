
from django.utils.timezone import localtime,datetime
from django.utils import timezone
#from dateutil.tz import *

def to_utc(date_time):
    if isinstance(date_time,str):
        date_time_obj = datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')
    else:
        date_time_obj = date_time 
    return date_time_obj - timezone.timedelta(hours=8)
    #return date_time_obj.replace(tzinfo=tzlocal()).astimezone(tzoffset(None, 0))

def localstr(date_obj):
    return localtime(date_obj).strftime('%Y-%m-%d %H:%M:%S')

