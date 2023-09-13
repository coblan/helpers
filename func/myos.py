import subprocess
import platform
from django.conf import settings
from helpers.func.dot_dict import read_dict_path

import logging
general_log = logging.getLogger('general_log')

def is_install(soft_name):
    p = subprocess.Popen(soft_name, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    #p = subprocess.Popen(soft_name, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    #p.wait()  
    stdout,erroutput = p.communicate()
    system_name = platform.system().lower()
    if getattr(settings,'VERBOSE_LOG',False):
        general_log.debug(system_name)
    
    try:
        if system_name == 'windows':
            #print("system = windows")
            #ww = p.stdout.read()
   
            #general_log.debug(ww)
            ww= stdout.decode('gbk')
            if getattr(settings,'VERBOSE_LOG',False):
                general_log.debug(ww)
            if '不是内部或外部命令' in ww:
                return False
            else:
                return True
           
        elif system_name == 'linux':
            #print('system = linux')
            #ww = p.stdout.read()
            #general_log.debug(ww)  
            ww= stdout.decode('utf-8') 
            if getattr(settings,'VERBOSE_LOG',False):
                general_log.debug(ww) 
            if 'not found' in ww:
                return False
            else:
                return True
    except Exception as e:
        general_log.exception(e)
        
        
       
    
    