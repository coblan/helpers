# encoding:utf-8
from __future__ import unicode_literals
from django.core.management.base import BaseCommand
from django.conf import settings
from helpers.director.base_data import inspect_dict
from helpers.director.models import PermitModel
from django.utils import timezone
import inspect
import os
import re

root_module=[]

used_module =[]
class Command(BaseCommand):
    """
    """
    def handle(self, *args, **options):
        out_str = "\n=========%s==========\n"%timezone.now()
        dc_str = ''
        gb_dict,local_dict={},{}
        if os.path.exists(settings.INSPECT_DICT_STATIC):
            with open( settings.INSPECT_DICT_STATIC,'r',encoding='utf-8') as f:
                org_str = f.read()
                if org_str:
                    exec(org_str,gb_dict,local_dict)
        
        global used_module
        for dc_name,dc in inspect_dict.items():
            out_ls = []
            org_dc = local_dict.get(dc_name)
            if org_dc:
                for k,v in dc.items():
                    # 防止 k的model没被记录到
                    value_str(k)
                    
                    if isinstance(v,(list,tuple)):
                        list_str = list_value_str(v)
          
                        if k not in org_dc:
                            out_ls.append('    %s\t:[%s],'%(value_str(k),list_str))
                        elif not isinstance(org_dc[k],(list,tuple))  or list_str != list_value_str( org_dc[k] ):
                            out_ls.append('    #?%s\t:[%s],'%(value_str(k),list_str))
                    else:
                        if k not in org_dc:
                            out_ls.append('    %s\t:%s,'%(value_str(k),value_str(v)))
                        elif value_str(v) != value_str( org_dc[k] ):
                            out_ls.append('    #?%s\t:%s,'%(value_str(k),value_str(v)))
                for k,v in org_dc.items():
                    if k not in dc:
                        # 去掉的 行，没必要 对象化
                        out_ls.append('    #-%s\t:%s,'%(value_str(k),str(v)))
            else:
                for k,v in dc.items():
                    if isinstance(v,(list,tuple)):
                        temp_ls=[]
                        for v_item in v:
                            temp_ls.append(value_str(v_item))
                        out_ls.append('    %s\t:[%s],'%(value_str(k),','.join(temp_ls)))
                    else:
                        out_ls.append('    %s\t:%s,'%(value_str(k),value_str(v)))
            
            if out_ls:
                dc_str += "\n%s = {\n%s\n}" %(dc_name+'_1' , '\n'.join(out_ls)  )
        new_module= list(set([x for x in used_module if x not in local_dict] ))
        rmd_module = list(set([x for x in local_dict.keys() if x not in used_module] ))
        for md in new_module:
            out_str +='\nimport %s'%md
        for md in rmd_module:
            if inspect.ismodule(local_dict.get(md)):
                out_str +='\n#-import %s'%md
        
        out_str += dc_str
            
                
        with open( settings.INSPECT_DICT_STATIC,'a+',encoding='utf-8') as f:
            f.write(out_str)
        
        
def value_str(v):
    #if inspect.isfunction(v):
    global used_module
    if isinstance(v,str):
        return '"%s"'%v
    else:
        used_module.append(value_mod(v))
        module = inspect.getmodule(v)
        return '%s.%s'%(module.__name__,v.__qualname__)

def list_value_str(v):
    temp_ls =[]
    for v_item in v:
        temp_ls.append(value_str(v_item))
    return ','.join(temp_ls)


def value_mod(v):
    module = inspect.getmodule(v)
    return module.__name__.split('.')[0]

def list_valude_mod(v):
    temp_ls=[]
    for v_item in v:
        temp_ls.append(value_mod(v_item))
    return temp_ls
    
    
