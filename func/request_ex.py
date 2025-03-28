from helpers.director.shortcut import get_request_cache
import time

def get_ip(request):
    '''获取请求者的IP信息'''
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')  # 判断是否使用代理
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]  # 使用代理获取真实的ip
    else:
        ip = request.META.get('REMOTE_ADDR')  # 未使用代理获取IP
    return ip

def request_time(name):
    resp = get_request_cache()
    if 'time_log' not in resp:
        resp['time_log'] = [{'time':time.time(),'name':name,'elapse':0}]
        return 0
    else:
        last = resp['time_log'][-1]
        now = time.time()
        resp['time_log'].append({'time':now,'name':name,'elapse':now-last['time']})
        return resp['time_log']