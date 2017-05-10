from django.http import HttpResponse
import json
from .wepay import JSApiWePay


def pay_replay(request):
    pay = JSApiWePay()
    xml_str = pay.reply(request)
    return HttpResponse(xml_str,content_type="text/xml")

def wepay_make_order(request):
    pay_type=request.GET.get('pay_type')
    if pay_type=='jsapi':
        pay = JSApiWePay()
        dc = pay.make_order()
    
    return HttpResponse(json.dumps(dc),content_type="application/json") 