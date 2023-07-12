import subprocess

import platform
import logging
general_log = logging.getLogger('general_log')

def is_install(soft_name):
    p = subprocess.Popen(soft_name, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    p.wait()    
    if platform.system().lower() == 'windows':
        print("windows")
        ww = p.stdout.read()
        ww= ww.decode('gbk')
        if '不是内部或外部命令' in ww:
            return False
        else:
            return True
       
    elif platform.system().lower() == 'linux':
        ww = p.stdout.read()
        ww= ww.decode('utf-8')      
        general_log.debug(ww)
        
        print('linux')
    
    