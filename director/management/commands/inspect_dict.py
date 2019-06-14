# encoding:utf-8
from __future__ import unicode_literals
from django.core.management.base import BaseCommand
from django.conf import settings
from helpers.director.base_data import site_cfg
from helpers.director.models import PermitModel
from django.utils import timezone
import inspect

class Command(BaseCommand):
    """
    """
    def handle(self, *args, **options):
        
        inspect_dict = site_cfg.get('inspect_dict')
        out_ls = []
        out_str = "\n=========%s==========\n"%timezone.now()
        with open( settings.STATIC_DICT,'r',encoding='utf-8') as f:
            org_str = f.read()
            gb_dict,local_dict={},{}
            if org_str:
                exec(org_str,gb_dict,local_dict)
            for dc_name,dc in inspect_dict.items():
                org_dc = local_dict.get(dc_name)
                if org_dc:
                    for k,v in dc.items():
                        if k not in org_dc:
                            out_ls.append('    "%s"\t:"%s",'%(k,value_str(v)))
                        elif value_str(v) != org_dc[k]:
                            out_ls.append('    "#?%s"\t:"%s",'%(k,value_str(v)))
                    for k,v in org_dc.items():
                        if k not in dc:
                            out_ls.append('    #-"%s"\t:"%s",'%(k,value_str(v)))
                else:
                    for k,v in dc.items():
                        out_ls.append('    "%s"\t:"%s",'%(k,value_str(v)))
                        
               
                if out_ls:
                    out_str += "\n%s = {\n%s\n}" %(dc_name , '\n'.join(out_ls)  )
                
        with open( settings.STATIC_DICT,'a+',encoding='utf-8') as f:
            f.write(out_str)
        
        
        
       
def value_str(v):
    if inspect.isfunction(v):
        return 'function: %s'%v.__name__
    else:
        return str(v)
    
