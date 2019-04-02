import base64
import qrcode
from io import BytesIO
from django.http import HttpResponse

def general_qr(request):
    """
    通用 qr，使用方式
    /d/qr?content=xxxxxxx&encode=base64
    """
    #args=get_argument(request)
    #kind=args.get('type')
    #if kind=='a':
        #content = args.get('content')
    #else:
        #content= base64.b64decode( args.get('content')).decode('utf-8')
    content = request.GET.get('content')
    encode=request.GET.get('encode')
    if encode=='base64':
        content=base64.b64decode(content)
    img=qrcode.make(content)
    byt=BytesIO()
    img.save(byt,'png')
    return HttpResponse(byt.getvalue(),content_type="image/png")   