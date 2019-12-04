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