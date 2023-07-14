from PIL import Image
from helpers.director.shortcut import director_element
from .url_path import media_url_to_path
import logging
general_log = logging.getLogger('general_log')
import imghdr
import subprocess
from helpers.func.myos import is_install
import os
from . url_path import set_suffix

png_compress = is_install('pngquant')
jpg_comporess = is_install('jpegoptim')
gif_comporess = is_install('gifsicle')

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


def compressImage(path,quality=None):
    imgType = imghdr.what(path)
    try:
        if imgType.lower() =='png':
            if not png_compress:
                general_log.debug('未安装pngquant,略过')
                return
            pngquant_compress(path,quality=quality)
        elif imgType.lower() in ['jpg','jpeg']:
            if not jpg_comporess:
                general_log.debug('未安装jpeg处理,略过')
                return 
            jpegoptim_compress(path,quality=quality)
        elif imgType.lower() =='gif':
            if not gif_comporess:
                general_log.debug('未安装gifsicle处理,略过')
                return 
            gifsicle_compress(path,quality=quality)
    except Exception as e:
        general_log.debug(f'压缩报错:{e}')

def pngquant_compress(path, force=False, quality=None,out_path=None):
    """压缩函数.
    
    参数：
        path: 文件名称
        force: 如果存在同名文件，是否覆盖
        quality: 压缩质量。 10-40， or 10
    """
    #force_command = '-f' if force else ''
    
    quality_command = ''
    if quality and isinstance(quality, int):
        quality_command = f'--quality {quality}'
    if quality and isinstance(quality, str):
        quality_command = f'--quality {quality}'
    if not out_path:
        command = f'pngquant {path} --skip-if-larger -f {quality_command} --output {path}'
    else:
        command = f'pngquant {path} --skip-if-larger -f {quality_command} --output {out_path}' 
    #subprocess.run(command)
    general_log.debug(f'压缩png图片{path}')
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    p.wait()
    general_log.debug(p.stdout.read())


def jpegoptim_compress(path,quality=70):
    general_log.debug(f'压缩jpg图片{path}')
    command = f'jpegoptim {path} -m{quality}'
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    p.wait()
    general_log.debug(p.stdout.read())    

def gifsicle_compress(path,quality=None):
    general_log.debug(f'压缩gif图片{path}')
    command = f'gifsicle -O3 {path} -o {path}'
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    p.wait()
    general_log.debug(p.stdout.read())     



def switch_format_check(media_path):
    path = media_url_to_path(media_path)
    org_size = os.stat(path).st_size
    imgType = imghdr.what(path)
    suf = imgType.lower()
    if suf =='png':
        new_file = change_to_jpg(path)
        jpegoptim_compress(path)
        new_size = os.stat(new_file).st_size
        if org_size > new_size:
            os.remove(path)
            return  set_suffix(media_path,'.jpg') # f'{media_path}.jpg'
        else:
            os.remove(new_file)
            return media_path
        
    elif suf in ['jpg','jpeg']:
        new_file = change_to_png(path)
        pngquant_compress(new_file)
        new_size = os.stat(new_file).st_size
        if org_size > new_size:
            os.remove(path)
            return  set_suffix(media_path ,'.png')  #f'{media_path}.png'   
        else:
            os.remove(new_file)
            return media_path  
    return media_path


def change_to_jpg(path):
    img = Image.open(path)
    img = img.convert("RGB")
    file_name=  set_suffix(path,'.jpg') # f'{path}.jpg'
    img.save(file_name)
    return file_name
    

def change_to_png(path):
    img = Image.open(path)
    file_name=  set_suffix(path,'.png') #  f'{path}.png'
    img.save(file_name)
    return file_name