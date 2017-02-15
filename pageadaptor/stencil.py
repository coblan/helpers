
from django.template import loader 
import re
import json

web_page_templates=[]

def regist(path,label):
    dc={}
    temp = loader.get_template(path)
    
    mt = re.search('<script .*form-meta-data[\'\"]>(.*)</script>',temp.template.source,re.M|re.S)
    
    if mt:
        code_str=mt.group(1)
        exec(code_str,dc)
        #dc = json.loads(code_str)
        del dc['__builtins__']
    dc.update({'value':path,'label':label})
    web_page_templates.append(dc)

