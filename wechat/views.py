from django.http import HttpResponse
import json
from .wepay.jsapi import JSApiWePay
from .wepay.appapi import APPApiWePay


def pay_replay(request):
    pay = JSApiWePay()
    xml_str = pay.reply(request)
    return HttpResponse(xml_str,content_type="text/xml")

def wepay_make_order(request):
    """
    GET:
    jsapi: /wechat/pay/new_order?pay_type=jsapi&openid=oIvmdwi8HWePf8rXFDA-jOpQL5uE
    appapi:/wechat/pay/new_order?pay_type=app
    """
    pay_type=request.GET.get('pay_type')
    if pay_type=='jsapi':
        pay = JSApiWePay()
        dc = pay.make_order(request)
    elif pay_type=='app':
        pay=APPApiWePay()
        dc=pay.make_order(request)
    return HttpResponse(json.dumps(dc),content_type="application/json") 