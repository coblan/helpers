import subprocess

import platform
import logging
general_log = logging.getLogger('general_log')

def is_install(soft_name):
    p = subprocess.Popen(soft_name, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    p.wait()   
    system_name = platform.system().lower()
    general_log.debug(system_name)
    
    try:
        if system_name == 'windows':
            print("system = windows")
            ww = p.stdout.read()
            #general_log.debug(ww)
            ww= ww.decode('gbk')
            general_log.debug(ww)
            if '不是内部或外部命令' in ww:
                return False
            else:
                return True
           
        elif system_name == 'linux':
            print('system = linux')
            ww = p.stdout.read()
            #general_log.debug(ww)  
            ww= ww.decode('utf-8') 
            general_log.debug(ww) 
            if 'not found' in ww:
                return False
            else:
                return True
    except Exception as e:
        general_log.exception(e)
        
        
       
    
    