import base64

from io import BytesIO
from django.http import HttpResponse

#def general_qr(request):
    #"""
    #通用 qr，使用方式
    #/d/qr?content=xxxxxxx&encode=base64
    #"""
    #import qrcode # 有时候没有安装 qrcode 模块
    ##args=get_argument(request)
    ##kind=args.get('type')
    ##if kind=='a':
        ##content = args.get('content')
    ##else:
        ##content= base64.b64decode( args.get('content')).decode('utf-8')
    #content = request.GET.get('content')
    #encode=request.GET.get('encode')
    #if encode=='base64':
        #content=base64.b64decode(content)
    #img=qrcode.make(content)
    #byt=BytesIO()
    #img.save(byt,'png')
    #return HttpResponse(byt.getvalue(),content_type="image/png")   

def general_qr(request):
    """
    通用 qr，使用方式
    /d/qr?content=xxxxxxx&encode=base64
    """
    import qrcode
    #from qrcode.image.styledpil import StyledPilImage  # 可选，用于更美观的样式
    
    content = request.GET.get('content')
    encode = request.GET.get('encode')
    
    if encode == 'base64':
        content = base64.b64decode(content).decode('utf-8')  # 确保解码为字符串
    
    # 创建 QRCode 对象并配置参数
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,      # 每个模块的像素大小
        border=1,         # 边距（模块数），设为 1 或 0 以减小边距
    )
    
    qr.add_data(content)
    qr.make(fit=True)
    
    # 生成图像（使用普通 PIL 图像或样式化图像）
    img = qr.make_image(fill_color="black", back_color="white")
    # 若需要更美观的样式，可替换为：
    #img = qr.make_image(image_factory=StyledPilImage)
    
    byt = BytesIO()
    img.save(byt, 'png')
    return HttpResponse(byt.getvalue(), content_type="image/png")