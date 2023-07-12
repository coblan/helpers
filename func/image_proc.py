from PIL import Image
from helpers.director.shortcut import director_element
from .url_path import media_url_to_path

@director_element('imageProc')
class ImageProc(object):
    def rotate(url):
        #读取图像
        im = Image.open("lenna.jpg")
        # 指定逆时针旋转的角度
        im_rotate = im.rotate(45) 


def ceil_image_size(inputpath,outpath,maxspan=1200,image_format=None,quality=50):
    "压缩图片"
    img = Image.open(inputpath)
    ratio = max(img.size) / maxspan
    if ratio >1:
        resized_image = img.resize(  (int(x / ratio) for x in img.size) )
        resized_image.save(outpath,image_format,quality=quality)