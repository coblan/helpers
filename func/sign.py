from django.utils import timezone
from helpers.director.shortcut import get_request_cache
from helpers.func.mymd5 import md5

def sign_check(salt,expire=60):
    """
    签名请求。
    header里面需要携带  
    ts:1677566658.1805983  以秒为单位的时间戳。 注意，js中Date.now()是毫秒为单位，所以需要除以1000
    sign: md5签名字符串
    
    """
    def __fun(fun):
        def _fun(*arg,**kws):
            request = get_request_cache()['request']
            sign = request.META.get('HTTP_SIGN')
            timestamp =  request.META.get('HTTP_TS') 
            if not timestamp:
                raise UserWarning("没有有效的时间戳")
            stamp = timezone.datetime.fromtimestamp(float(timestamp))
            if timezone.now() - stamp > timezone.timedelta(seconds=expire):
                raise UserWarning("请求已经过期")
            ls = []
            tmp_kws = dict(kws)
            tmp_kws['ts'] = timestamp
            for k,v in tmp_kws.items():
                if isinstance(v,list) or isinstance(v,dict):
                    continue
                ls.append(f'{k}={v}')
            ls.sort()
            url = '&'.join(ls)
            url += f'&salt={salt}'
            #url = f'amount={amount}&app={app}&userid={userid}&username={username}&salt={salt}'
            sign_str = md5(url)
            if sign_str != sign:
                raise UserWarning(f'签名不正确,服务器签名串:{url};签名串MD5为{sign_str}。客户端上传签名串MD5为{sign}')
            return fun(*arg,**kws)
        return _fun
    return __fun