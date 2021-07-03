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

class BasicReciever(object):
    
    def asView(self,request):
        self.request = request
        file_dict = request.FILES
        file_url_list=[]
        for name, fl in file_dict.items():
            file_data= self.readFile(fl)
            file_url = self.procFile(file_data,fl)
            file_url_list.append(file_url)
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
        file_path = os.path.join(par_dir,file_name)
        
        absolut_par_path = os.path.join( settings.MEDIA_ROOT, par_dir)
        try:
            os.makedirs(absolut_par_path)
        except os.error as e:
            print(e)   
        
        absolut_file_path =os.path.join(absolut_par_path,file_name)

        with open(absolut_file_path,'wb') as general_file:
            general_file.write(file_data)
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

class GeneralUpload(BasicReciever):
    """
    @path: media的相对路径
    @split: month ;date
    @keepname: 1
    """
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







