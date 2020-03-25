
from django.core.management.base import BaseCommand
from django.conf import settings
from helpers.director.base_data import doc_dict

from django.utils import timezone
import inspect
import os
import re

class Command(BaseCommand):
    """
    """
    def add_arguments(self, parser):
        parser.add_argument('--tag', nargs='+', type=str)
        
    def handle(self, *args, **options):
        target_tags = options.get('tag')
        if not target_tags:
            target_tags = ['api']
        root_file =  os.path.join(os.path.dirname(settings.BASE_DIR),'doc','source')   
        for file_key,doc_list in doc_dict.items():
            file_path = os.path.join(root_file,file_key)
            docs =[]
            for item in doc_list:
                for tag in item.get('tag'):
                    if tag in target_tags:
                        docs.append(item)
                        break
            docs = sorted(docs,key= lambda x: x.get('sort') )
            content = ''.join([x.get('text') for x in docs])
            
            with open(file_path,'w',encoding='utf-8') as f:
                f.write(content)
               
        
        

    
    
