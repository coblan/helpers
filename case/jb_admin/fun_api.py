from helpers.director.shortcut import director_view
import urllib
from helpers.func import ex
from django.conf import settings
import os
@director_view('save/dataurl/png')
def save_dataurl_png(dataurl):
    response = urllib.request.urlopen(dataurl)
    parent_path = os.path.join(settings.MEDIA_ROOT, 'convert')
    try:
        os.makedirs(parent_path)
    except Exception:
        pass
    file_name = ex.md5(dataurl) +'.png'
    abs_file_path = os.path.join(parent_path, file_name)
    with open(abs_file_path, 'wb') as f:
        f.write(response.file.read())
    return settings.MEDIA_URL +'/convert/%s'%file_name