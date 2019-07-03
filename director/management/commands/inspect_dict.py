# encoding:utf-8
from __future__ import unicode_literals
from django.core.management.base import BaseCommand
from django.conf import settings
from helpers.director.base_data import site_cfg
from helpers.director.models import PermitModel
from django.utils import timezone
import inspect
import os
import re

root_module=[]

class Command(BaseCommand):
    """
    """
    def handle(self, *args, **options):
        
        inspect_dict = site_cfg.get('inspect_dict')
        
        out_str = "\n=========%s==========\n"%timezone.now()
        dc_str = ''
        gb_dict,local_dict={},{}
        if os.path.exists(settings.INSPECT_DICT_STATIC):
            with open( settings.INSPECT_DICT_STATIC,'r',encoding='utf-8') as f:
                org_str = f.read()
                if org_str:
                    exec(org_str,gb_dict,local_dict)
        
        used_module =[]
        for dc_name,dc in inspect_dict.items():
            out_ls = []
            org_dc = local_dict.get(dc_name)
            if org_dc:
                for k,v in dc.items():
                    used_module.append(value_mod(v))
                    if k not in org_dc:
                        out_ls.append('    "%s"\t:%s,'%(k,value_str(v)))
                    elif value_str(v) != value_str( org_dc[k] ):
                        out_ls.append('    "#?%s"\t:%s,'%(k,value_str(v)))
                for k,v in org_dc.items():
                    if k not in dc:
                        out_ls.append('    #-"%s"\t:%s,'%(k,value_str(v)))
            else:
                for k,v in dc.items():
                    if isinstance(v,(list,tuple)):
                        temp_ls=[]
                        for v_item in v:
                            used_module.append(value_mod(v_item))
                            temp_ls.append(value_str(v_item))
                        out_ls.append('    "%s"\t:[%s],'%(k,','.join(temp_ls)))
                    else:
                        used_module.append(value_mod(v))
                        out_ls.append('    "%s"\t:%s,'%(k,value_str(v)))
            
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
    module = inspect.getmodule(v)
    
    return '%s.%s'%(module.__name__,v.__qualname__)

def value_mod(v):
    module = inspect.getmodule(v)
    return module.__name__.split('.')[0]
        #fun_repre = repr(v)
        #mt = re.search('^(.*) at ',fun_repre)
        #return mt.group(1)+'>'
    #elif isinstance(v,(list,tuple)):
        #return [value_str(x) for x in v]
    #else:
        #return str(v)
    
