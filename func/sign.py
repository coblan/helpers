from django.utils import timezone
from helpers.director.shortcut import get_request_cache
from helpers.func.mymd5 import md5
from django.conf import settings

def sign_check(salt,expire=60):
    """
    签名请求。
    请求时需要使用参数签名，参数包括GET中的url上挂在的参数，POST中body中传递的参数。需要剔除掉数组，对象以及文件这些不能严谨的转换为字符串的参数。
    
    参数根据参数名**排序**后，拼接成url，**最后**添加上salt和ts，构成最终url，计算url的md5值，就是签名字符串。
    签名信息：
    sign=md5( 'path=video&username=test&salt=12345&ts=1677652614')
    其中：
        ts:1677566658.1805983  以秒为单位的时间戳。 注意，js中Date.now()是毫秒为单位，所以需要除以1000
        salt:签名的key
    
    最后将签名信息放在header里面，请求服务器。
    header中增加
        {
	    ts:1677652614
            sign:"1980DF99E7C442EFBCAAA2759DC85F24"
        }
    
       
    
    """
    def __fun(fun):
        def _fun(*arg,**kws):
            request = get_request_cache()['request']
            sign = kws.pop('sign',None) or  request.META.get('HTTP_SIGN')
            timestamp = kws.pop('ts',None) or request.META.get('HTTP_TS') 
            if not timestamp:
                raise UserWarning("没有有效的时间戳")
            stamp = timezone.datetime.fromtimestamp(float(timestamp))
            if timezone.now() - stamp > timezone.timedelta(seconds=expire):
                raise UserWarning("请求已经过期")
            ls = []
            tmp_kws = dict(kws)
            for k,v in tmp_kws.items():
                if isinstance(v,list) or isinstance(v,dict):
                    continue
                ls.append(f'{k}={v}')
            ls.sort()
            url = '&'.join(ls)
            no_salt_url = url + f'&salt={{salt}}&ts={timestamp}'
            url += f'&salt={salt}&ts={timestamp}'
            #url = f'amount={amount}&app={app}&userid={userid}&username={username}&salt={salt}'
            sign_str = md5(url)
            if sign_str != sign:
                if settings.DEBUG:
                    raise UserWarning(f'签名不正确,服务器签名串:{url};签名串MD5为{sign_str}。客户端上传签名串MD5为{sign}')
                else:
                    raise UserWarning(f'签名不正确,服务器签名串:{no_salt_url};签名串MD5为{sign_str}。客户端上传签名串MD5为{sign}')
            return fun(*arg,**kws)
        return _fun
    return __fun


def sign_check_version0(salt,expire=60,):
    """
    签名请求。
    请求时需要使用参数签名，参数包括GET中的url上挂在的参数，POST中body中传递的参数。需要剔除掉数组，对象以及文件这些不能严谨的转换为字符串的参数。
    
    参数根据参数名**排序**后，拼接成url，**最后**添加上salt，构成最终url，计算url的md5值，就是签名字符串。
    签名信息：
    sign=md5( 'path=video&username=test&salt=12345&ts=1677652614')
    其中：
        ts:1677566658.1805983  以秒为单位的时间戳。 注意，js中Date.now()是毫秒为单位，所以需要除以1000
        salt:签名的key
    
    最后将签名信息放在header里面，请求服务器。
    header中增加
        {
            ts:1677652614
            sign:"1980DF99E7C442EFBCAAA2759DC85F24"
        }
    
       
    
    """
    def __fun(fun):
        def _fun(*arg,**kws):
            request = get_request_cache()['request']
            sign = kws.pop('sign',None) or  request.META.get('HTTP_SIGN')
            timestamp = kws.pop('ts',None) or request.META.get('HTTP_TS') 
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