from __future__ import unicode_literals

from django.http import HttpResponse
from django.conf import settings
import os
from datetime import datetime
import json
import hashlib
import io
import urlparse
import hashlib
from django.views.decorators.csrf import csrf_exempt

try:
    general_upload= os.path.join(settings.MEDIA_ROOT,'general_upload')
    os.makedirs(general_upload)
except os.error:
    pass

def general(request):
    file_dict = request.FILES
    file_dir=general_upload
    file_url_list=[]
    for name, fl in file_dict.items():
        catch = io.BytesIO()
        m = hashlib.md5()        
        for chunk in fl.chunks():
            catch.write(chunk) 
            m.update(chunk)    
            
        catch.flush()
        file_name=m.hexdigest()+'_'+fl.name
        file_path=os.path.join(file_dir,file_name)
        if not os.path.exists( file_path ):
            with open(file_path,'wb') as general_file:
                general_file.write(catch.getvalue())
                
        file_url=urlparse.urljoin(settings.MEDIA_URL, 'general_upload/{file_name}'.format(file_name=file_name))
        file_url_list.append(file_url)
    
    return HttpResponse(json.dumps(file_url_list),content_type="application/json")