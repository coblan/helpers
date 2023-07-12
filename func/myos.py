import subprocess

import platform
import logging
general_log = logging.getLogger('general_log')

def is_install(soft_name):
    p = subprocess.Popen(soft_name, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    p.wait()   
    system_name = platform.system().lower()
    general_log.debug(system_name)
    
    if system_name == 'windows':
        print("windows")
        ww = p.stdout.read()
        general_log.debug(ww)
        ww= ww.decode('gbk')
        
        if '不是内部或外部命令' in ww:
            return False
        else:
            return True
       
    elif system_name == 'linux':
        print('linux')
        ww = p.stdout.read()
        general_log.debug(ww)  
        ww= ww.decode('utf-8') 
        if 'not found' in ww:
            return False
        else:
            return True
        
        
       
    
    