# encoding:utf-8

from __future__ import unicode_literals

from django.http import HttpResponse
from django.conf import settings
import os
from django.utils.timezone import datetime
import json
import hashlib
import io
import urlparse
import hashlib
import re
from django.views.decorators.csrf import csrf_exempt

class BasicReciever(object):
    
    
    def asView(self,request):
        file_dict = request.FILES
        file_url_list=[]
        for name, fl in file_dict.items():
            file_data= self.readFile(fl)
            file_url = self.procFile(file_data,name)
            file_url_list.append(file_url)
        return HttpResponse(json.dumps(file_url_list),content_type="application/json")
    
    def readFile(self,fl):
        catch = io.BytesIO()       
        for chunk in fl.chunks():
            catch.write(chunk)  
        catch.flush()
        return catch.getvalue()
    
    def procFile(self,file_data,name):
        file_path,file_name = self.getFilePath(file_data,name)
        with open(file_path,'wb') as general_file:
            general_file.write(file_data)
            return self.getFileUrl(file_name)
        

    def getFilePath(self,file_data,name):
        par_dir = self.getParDir()
        sufix = self.getSufix(name)
        m = hashlib.md5()   
        m.update(file_data)  
        mid_name = m.hexdigest()
        file_name = mid_name+'.'+sufix
        return os.path.join(par_dir,file_name),file_name
    
    def getParDir(self):
        try:
            par_path= os.path.join(settings.MEDIA_ROOT,'general_upload')
            os.makedirs(par_path)
        except os.error:
            pass   
        return par_path
    
    def getSufix(self,name):
        mt_name=re.search('\.(\w+)$',name)
        if mt_name:
            return mt_name.group(1)
        else:
            return ''
            #file_name=m.hexdigest()+'___'+fl_name
        #else:
            ## 没有后缀名的img,使用md5.png的形式来标记它
            #img_ext = re.search('image/(\w+)',fl.content_type)
            #if img_ext:
                #file_name =m.hexdigest()+'.'+img_ext.group(1)
            #else:
                #file_name=m.hexdigest()        
    
    def getFileUrl(self,file_name):
        file_url=urlparse.urljoin(settings.MEDIA_URL, 'general_upload/{file_name}'.format(file_name=file_name))
        return  file_url

class RecieverWithTimeSplit(BasicReciever):
    def getParDir(self):
        today = datetime.today().date()
        today_str  = today.strftime('%Y_%m_%d')        
        try:
            par_path= os.path.join(settings.MEDIA_ROOT,'general_upload',today_str)
            os.makedirs(par_path)
        except os.error:
            pass 
        return par_path  




#def general(request):
    #file_dict = request.FILES
    #par_path,par_dir= get_par_path() #general_upload
    #file_url_list=[]
    #for name, fl in file_dict.items():
        #catch = io.BytesIO()
        #m = hashlib.md5()        
        #for chunk in fl.chunks():
            #catch.write(chunk) 
            #m.update(chunk)    
            
        #catch.flush()
        
        #fl_name =adapt_name(name)
        #mt_name=re.search('\.(\w+)$',fl_name)
        #if mt_name:
            #file_name=m.hexdigest()+'___'+fl_name
        #else:
            ## 没有后缀名的img,使用md5.png的形式来标记它
            #img_ext = re.search('image/(\w+)',fl.content_type)
            #if img_ext:
                #file_name =m.hexdigest()+'.'+img_ext.group(1)
            #else:
                #file_name=m.hexdigest()
        
        
        #file_path=os.path.join(par_path,file_name)
        #if not os.path.exists( file_path ):
            #with open(file_path,'wb') as general_file:
                #general_file.write(catch.getvalue())
                
        #file_url=urlparse.urljoin(settings.MEDIA_URL, 'general_upload/{par_dir}/{file_name}'.format(par_dir=par_dir,file_name=file_name))
        #file_url_list.append(file_url)
    
    #return HttpResponse(json.dumps(file_url_list),content_type="application/json")



#def adapt_name(fl_name):
    #mt = re.search('\w+___(.+)',fl_name)
    #if mt:
        #return mt.group(1)
    #else:
        #return fl_name

