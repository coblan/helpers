# encoding:utf-8

from __future__ import unicode_literals

from django.http import HttpResponse
from django.conf import settings
import os
from django.utils.timezone import datetime
import json
import hashlib
import io
from urllib.parse import urljoin
import hashlib
import re
from django.views.decorators.csrf import csrf_exempt
from helpers.director.base_data import director
import time
from helpers.func.image_proc import ceil_image_size,compressImage,switch_format_check
from helpers.director.shortcut import director_view
from helpers.func.url_path import media_url_to_path
from helpers.func.dot_dict import read_dict_path
import logging
general_log = logging.getLogger('general_log')

class BasicReciever(object):
    
    def asView(self,request):
        self.request = request
        file_dict = request.FILES
        file_url_list=[]
        for name, fl in file_dict.items():
            file_data= self.readFile(fl)
            file_url = self.procFile(file_data,fl)
            file_url_list.append(file_url)
        file_url_list = [ self.switch_format_check(media_path) for media_path in file_url_list]
        file_url_list = self.encrypt(file_url_list)
        return HttpResponse(json.dumps(file_url_list),content_type="application/json")
    
    def readFile(self,fl):
        catch = io.BytesIO()       
        for chunk in fl.chunks():
            catch.write(chunk)  
        catch.flush()
        return catch.getvalue()
    
    def procFile(self,file_data,fl):
        par_dir = self.getParDir()
        file_name = self.getFileName(file_data,fl)
        file_name = file_name.lower()
       
        #if not any([x in file_name for x in ['.jpeg','jpg','png'] ]):
        # 文件没有后缀的情况下
        if '.' not in file_name: 
            if 'image' in fl.content_type: 
                file_name +=  '.' +fl.content_type.split('/')[-1]
        file_path = os.path.join(par_dir,file_name)
        
        absolut_par_path = os.path.join( settings.MEDIA_ROOT, par_dir)
        try:
            os.makedirs(absolut_par_path)
        except os.error as e:
            print(e)   
        
        absolut_file_path =os.path.join(absolut_par_path,file_name)

        with open(absolut_file_path,'wb') as general_file:
            general_file.write(file_data)
        if self.request.GET.get('maxspan'):
            span = int( self.request.GET.get('maxspan') )
            # 压缩图片的 width 和height
            ceil_image_size(absolut_file_path,absolut_file_path,maxspan= span )
            compressImage(absolut_file_path)
        
        elif self.request.GET.get('quality'):
            quality = self.request.GET.get('quality')
            compressImage(absolut_file_path,quality)
            
        return self.getFileUrl(file_path)
        
    
    def getFileName(self,file_data,fl):
        sufix = self.getSufix(fl)
        m = hashlib.md5()   
        m.update(file_data)  
        mid_name = m.hexdigest()
        file_name = mid_name+'.'+sufix
        return file_name
    
    def getParDir(self):
        return 'general_upload'
        #try:
            #par_path= os.path.join(settings.MEDIA_ROOT,'general_upload')
            #os.makedirs(par_path)
        #except os.error:
            #pass   
        #return par_path
    
    def getSufix(self,fl):
        mt_name=re.search('\.(\w+)$',fl.name)
        if mt_name:
            return mt_name.group(1)
        else:
            return fl.content_type.split('/')[-1]
    def getFileUrl(self,file_name):
        file_url=urljoin(settings.MEDIA_URL, 'general_upload/{file_name}'.format(file_name=file_name))
        return  file_url
    
    def isImage(self,fl):
        if 'image' in fl.content_type: 
            return True
        for sufix in ['.png','.jpg']:
            if sufix in fl.name.lower():
                return True
        else:
            return False
    
    def getImageFormat(self,fl):
        suffix = None
        if 'image' in fl.content_type: 
            suffix = fl.content_type.split('/')[-1] 
        return suffix
    
    def switch_format_check(self,media_path):
        if self.request.GET.get('sfc'):
            return switch_format_check(media_path,model =int( self.request.GET.get('sfc') ))
        else:
            return media_path
    
    def encrypt(self,file_url_list):
        if self.request.GET.get('aes'):
            from . funs.aes import encode_file
            ls = []
            for media_url in file_url_list:
                ls.append(encode_file(media_url))
                try: 
                    path  = media_url_to_path(media_url)
                    os.remove(path)
                except Exception as e:
                    general_log.debug(e)
            file_url_list = ls
        return file_url_list
    
    


class GeneralUpload(BasicReciever):
    """
    @path: media的相对路径
    @split: month ;date
    @keepname: 1
    """
    
    #def readFile(self, fl):
        #image_data =  super().readFile(fl)
        #from PIL import Image
        #img = Image.open(io.BytesIO(image_data))    
        #print('hell')
        #return img.tobytes()
        
        
    
    def getParDir(self):
        path = self.request.GET.get('path','general_upload')
        split = self.request.GET.get('split','')
        today = datetime.today().date()
        if split=='month' or \
           (split =='' and path.startswith('general_upload')):
            # 对于以前的上传路径，统一增加默认split=month是更加合理的
            # 如果遇到用户自定义了path，应该都不是以 general_upload 开始,所以排除开split默认值的影响
            path = os.path .join(path,today.strftime('%Y_%m'))
        elif split =='date':
            path = os.path.join(path,today.strftime('%Y_%m_%d'))
        return path
    
    def getFileName(self,file_data,name):
        sufix = self.getSufix(name)
        m = hashlib.md5()   
        m.update(file_data)  
        mid_name = m.hexdigest()
        
        file_name = mid_name+'.'+sufix
        if self.request.GET.get('keepname'):
            fl_name =self.adapt_name(name)
            mt_name=re.search('\.(\w+)$',fl_name)
            if mt_name:
                file_name=mid_name+'___'+fl_name
        return file_name   
    
    def getFileUrl(self,file_path):
        file_url = file_path.replace('\\', '/')
        absolute_file_url=urljoin(settings.MEDIA_URL, file_url)
        return  absolute_file_url    
    
    def adapt_name(fl_name):
        """
        为了防止循环保存一个文件，造成文件名不断变长,只截取最后一段名字
        """
        mt = re.search('\w+___(.+)',fl_name)
        if mt:
            return mt.group(1)
        else:
            return fl_name   
        

        

def get_md5(text):
    m = hashlib.md5()   
    m.update(text.encode('utf-8'))  
    mid_name = m.hexdigest()
    return mid_name
    
class BigFileRecieve(GeneralUpload):
    def asView(self,request):
        self.request = request
        file_dict = request.FILES
        file_url_list=[]

        for name, fl in file_dict.items():
            """
            @name:字段名称
            @fl:文件对象。 
              fl.name 是文件的上传名
            """
            keepname = request.GET.get('keepname','tm-name')
            if keepname =='field_name':
                file_name = name
            elif keepname=='overwrite':
                file_name = fl.name
            elif keepname=='overwrite-md5':
                sufix = self.getSufix(fl)
                file_name = get_md5(fl.name)+'.'+ sufix 
            elif keepname=='tm-name':
                file_name = '%s_%s'%(int( time.time()%1000000),fl.name)
            elif keepname =='tm-md5':
                sufix = self.getSufix(fl)
                file_name = '%s_%s.%s'%(int( time.time()%1000000),get_md5( fl.name),sufix )
            par_dir = self.getParDir()
            file_path = os.path.join(par_dir,file_name)            
            absolut_par_path = os.path.join( settings.MEDIA_ROOT, par_dir)
            try:
                os.makedirs(absolut_par_path)
            except os.error as e:
                print(e)   
            absolut_file_path =os.path.join(absolut_par_path,file_name)
            with open(absolut_file_path,'wb') as general_file:
                for chunk in fl.chunks():
                    general_file.write(chunk)
            
            if self.isImage(fl):
                suffix = self.getImageFormat(fl)
                self.processImage(absolut_file_path,image_format = suffix)
            
            file_url = self.getFileUrl(file_path)
            file_url_list.append(file_url)
            
        file_url_list = [ self.switch_format_check(media_path) for media_path in file_url_list]
        #self.file_url_list = file_url_list
        self.file_url_list = self.encrypt(file_url_list)
        return HttpResponse(json.dumps(file_url_list),content_type="application/json")
    
    def processImage(self,absolut_file_path,image_format=None):
        if self.request.GET.get('maxspan'):
            span = int( self.request.GET.get('maxspan') )
            # 压缩图片的 width 和height
            ceil_image_size(absolut_file_path,absolut_file_path,maxspan= span,image_format=image_format )
            if self.request.GET.get('quality'):
                quality = self.request.GET.get('quality')
                compressImage(absolut_file_path,quality)  
            else:
                compressImage(absolut_file_path)
        
        elif self.request.GET.get('quality'):
            quality = self.request.GET.get('quality')
            compressImage(absolut_file_path,quality)        

director.update({
    'big-file-saver':BigFileRecieve
})
#class RecieverWithTimeSplit(BasicReciever):
    #def getParDir(self):
        #today = datetime.today().date()
        #today_str  = today.strftime('%Y_%m_%d')        
        #try:
            #par_path= os.path.join(settings.MEDIA_ROOT,'general_upload',today_str)
            #os.makedirs(par_path)
        #except os.error:
            #pass 
        #return par_path  

@director_view('media/file/merge')
def merge_media_file(path_list,suffix=None):
    """
    分块上传后，调用改接口合并成一个文件
    """
    #if target:
        #if not target.startswith('/media/'):
            #if target.startswith('/'):
                #target =  '/media' + target
            #else:
                #target =  '/media/' + target
    if suffix:
        if suffix.startswith('.'):
            target = path_list[0] + suffix
        else:
            target = path_list[0]+'.' + suffix
    else:
        target = path_list[0]
    abs_target = media_url_to_path(target)
    with open(abs_target,'wb+') as f:
        for path in path_list:
            abs_path = media_url_to_path(path) #  os.path.join(settings.MEDIA_ROOT,path.lstrip('/media/'))
            with open(abs_path,'rb') as f_slice:
                dt = f_slice.read()
                f.write(dt)
            os.remove(abs_path)
    
    return target
            
@director_view('upload/encrypt/info')
def encrypt_aes_info(entry):
    """
    前端picture组件，遇到aes文件时，直接调用这个函数获取加密设置。免得一个一个去设置组件参数
    """
    dc =  read_dict_path(settings, f'UPLOAD_CRYPTO.{entry}')
    return dc



