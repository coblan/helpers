import datetime
beijin = datetime.timezone(datetime.timedelta(hours=8))
utc = datetime.timezone(datetime.timedelta(hours=0))
def tm2mongo(dt):
    if not dt:
        return dt
    tmp = dt.replace(tzinfo=beijin)
    return tmp

def mongo2tm(dt):
    if not dt:
        return dt
    dd = dt.replace(tzinfo=utc)
    return dd.astimezone(beijin)