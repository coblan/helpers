import base64
from Crypto.Cipher import AES     #注：python3 安装 Crypto 是 pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple pycryptodome<br><br>
#解密
from Crypto.Util.Padding import pad, unpad
import re
import os
from helpers.func.url_path import media_url_to_path
from helpers.director.shortcut import director_view
import logging
general_log = logging.getLogger('general_log')
from django.conf import settings
from helpers.func.dot_dict import read_dict_path

import hashlib

padding = lambda s: s + (16 - len(s) % 16) * chr(16 - len(s) % 16) .encode('utf-8')
#加密
def aes_encode_byte(data, key):
    #while len(data) % 16 != 0:     # 补足字符串长度为16的倍数
        #data += (16 - len(data) % 16) * chr(16 - len(data) % 16)
    #data = str.encode(data)
    aes = AES.new(str.encode(key), AES.MODE_ECB)  # 初始化加密器
    BLOCK_SIZE =  16 #32    
    return aes.encrypt(  pad(data, BLOCK_SIZE)  )

   # wang xiang 要求的这个，现在解密有问题，展示屏蔽了试试。
    #return aes.encrypt(  padding(data)  )
    
    #return str(base64.encodebytes(aes.encrypt(data)), encoding='utf8').replace('\n', '')  # 加密

def aes_decode_byte(data, key):
    aes = AES.new(str.encode(key), AES.MODE_ECB)  # 初始化加密器
    decrypted_byte = aes.decrypt(data)  # 解密
    decrypted_byte = unpad(decrypted_byte, 16)  # 32去除多余补位
    return decrypted_byte

def aes_encode_str(string,key):
    bb= aes_encode_byte(string.encode('utf-8'),key)
    return base64.b64encode(bb)

@director_view('aes/file')
def encode_file(media_path,after_del=True):
    """
    加密当前路径文件
    """
    #key = '94a4b778g01ca4ab'
    if not media_path:
        return media_path
    key = read_dict_path(settings.UPLOAD_CRYPTO,'aes.key')
    try:
        path = media_url_to_path(media_path)
        if path.endswith('.aes'):
            return media_path
    except Exception as e:
        general_log.exception(e)
        return
    if not os.path.exists(path):
        general_log.debug(f'路径不存在：{path}')
        return 
    
    with open (path,'rb') as f:
        data = f.read()
        rt = aes_encode_byte(data,key)
        mt= re.search('\.\w+$',path)
        if mt:
            aes_path = f'{path[0:-len(mt.group())]}.aes'
            aes_url = f'{media_path[0:-len(mt.group())]}.aes'
        else:
            aes_path = f'{path}.aes'
            aes_url = f'{media_path}.aes'
        with open (aes_path,'wb') as f2:
            f2.write(rt)
    if after_del:
        os.remove(path)
        general_log.debug(f'加密后,删除文件{path}')
    return aes_url


def decode_file_content(media_path):
    key = read_dict_path(settings.UPLOAD_CRYPTO,'aes.key')
    path = media_url_to_path(media_path)

    with open (path,'rb') as f:
        data = f.read()
        rt = aes_decode_byte(data,key)
        return rt
        
@director_view('aes-decode/file')
def decode_file(media_path):
    """
    解密当前路径文件
    """
    #key = '94a4b778g01ca4ab'
    if not media_path:
        return media_path
    key = read_dict_path(settings.UPLOAD_CRYPTO,'aes.key')
    try:
        path = media_url_to_path(media_path)
    except Exception as e:
        general_log.exception(e)
        return
    if not os.path.exists(path):
        general_log.debug(f'路径不存在：{path}')
        return 
    
    with open (path,'rb') as f:
        data = f.read()
        rt = aes_decode_byte(data,key)
      
        #mt= re.search('\.\w+$',path)
        #if mt:
            #aes_path = f'{path[0:-len(mt.group())]}.aes'
            #aes_url = f'{media_path[0:-len(mt.group())]}.aes'
        #else:
            #aes_path = f'{path}.aes'
            #aes_url = f'{media_path}.aes'
        if path.endswith('.aes'):
            # 获取.jpg.aes中的.jpg作为文件后缀
            aes_path =path[:-4]
            aes_url = media_path[:-4]
        else:
            aes_path =path
            aes_url = media_path         
        with open (aes_path,'wb') as f2:
            f2.write(rt)
        return aes_url

class AesHtml(object):
    def __init__(self,aes_files=None):
        """
        aes_files={
            'ASDFSGASG':/media/xxx.aes
        }
        """
        self.aes_files = aes_files
        
    def run(self,html):
        from bs4 import BeautifulSoup
        self.html = html
        soup = BeautifulSoup(html)
        for image in soup.select('img'):
            if  self.aes_files and image.attrs.get('src').startswith('data:image/png;base64,'):
                md = hashlib.md5()
                md.update( image.attrs['src'].encode('utf-8') )
                key = md.hexdigest()
                image.attrs['src'] = self.aes_files.get(key )            
            elif image.attrs['src'].startswith('/media'):
                png_src = image.attrs['src']
                #if png_path :''.endswith(('.jpg','.jpeg','.gif','.png','.webp'))
                if not png_src.endswith('.aes'):
                    image.attrs['src'] = self.aesImage(png_src)
                    
                    # 删除原图  [现在已经在encode_file函数里面删除原始文件了，这里就不需要再删除了。]
                    #png_path = media_url_to_path(png_src)
                    #os.remove(png_path)
                
        return  str(soup)
        
    def aesImage(self,media_url):
        aes_url = encode_file(media_url)
        return aes_url

class UnAesHtml(object):
    def __init__(self):
        self.aes_files={}
        
    def run(self,html):
        from bs4 import BeautifulSoup
        self.html = html
        soup = BeautifulSoup(html)
        for image in soup.select('img'):
            if image.attrs.get('src').endswith('.aes'):
                old_str = image.attrs['src']
                image.attrs['src'] = self.decodeAesImage(image.attrs['src'])
                md = hashlib.md5()
                md.update( image.attrs['src'].encode('utf-8') )
                key = md.hexdigest()
                self.aes_files[ key] = old_str
        return  str(soup)
        
    def decodeAesImage(self,media_url):
        try:
            aes_url = decode_file_content(media_url)
            base_str= base64.b64encode(aes_url).decode('utf-8')
            aes_url = 'data:image/png;base64,'+base_str             
        except Exception as e:
            general_log.debug('decode aes error:',str(e)) 
            aes_url = media_url
        
        return aes_url 
    
if __name__ == '__main__':
    key = '94a4b778g01ca4ab'  # 密钥长度必须为16、24或32位，分别对应AES-128、AES-192和AES-256
    #data = "E83A56F6BCF88E5BD3600C398E39EAAFA91DBA24807B73F7B76FF1E180CEA14DAED6A43F9304901044C50503198C2D3A57661"    # 待加密文本
    
    #with open (r'C:\Users\heyul\Desktop\tmp\password\1e5031a72b9213325a0edfd140394cf5.png','rb') as f:
        #data = f.read()
        #rt = aes_encode_byte(data,key)
        #with open (r'C:\Users\heyul\Desktop\tmp\password\test_image.aes','wb') as f2:
            #f2.write(rt)
            
            
    #mi = aes_encode(data,key)
    #print("加密值：",mi)
    #print("解密值：",aes_decode(mi,key))
    
    with open(r'C:\Users\heyul\Desktop\tmp\password\test_image.aes','rb') as f:
        data = f.read()
        ppdata = aes_decode_byte(data,key)
        with open (r'C:\Users\heyul\Desktop\tmp\password\after_image.png','wb') as f2:
            f2.write(ppdata)