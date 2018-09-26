import requests
from helpers.func.random_str import get_str
from django.conf import settings
import time
import hashlib
import json

import logging
log = logging.getLogger('middle_result')

def send_validate_code(phone,  code , last_minits = 3): 
    strRand = get_str(10)
    time_now =  int(time.time())
    validate_temp = settings.TENCENT.get('validate_temp')
    args = {
        'sdkappid': settings.TENCENT.get('SdkAppId'),
        'strRand': strRand,
        'appkey': settings.TENCENT.get('AppKey'),
        "time": time_now,
        'phone': phone,
    }
    
    
    api_url = 'https://yun.tim.qq.com/v5/tlssmssvr/sendsms?sdkappid=%(sdkappid)s&random=%(strRand)s' % args
    
    sig_str = 'appkey=%(appkey)s&random=%(strRand)s&time=%(time)s&mobile=%(phone)s' % args
    
    hash = hashlib.sha256()
    hash.update(sig_str.encode('utf-8'))
    siged = hash.hexdigest()   
    
    dc = {
        "ext": "",
            "extend": "",
            "params": [
                code,
                last_minits
            ],
            "sig": siged,
            "sign": "腾讯云",
            "tel": {
                "mobile": phone,
                "nationcode": "86"
            },
            "time": time_now,
            "tpl_id": validate_temp  
    }
    log.info('手机号码：%(phone)s 发送验证码%(code)s' % {'phone': phone, 'code': code,})
    rt = requests.post(api_url, json.dumps(dc) )
    log.info( rt.text )
    #print(rt.text)
    """ '{"result":0,"errmsg":"OK","ext":"","sid":"18:89980144e3b04b0bbc2282504069c1ea","fee":1}' """
    #rt_dc = json.loads(rt.text)
    