from django.conf import settings
import os

def media_url_to_path(url):
    '''将本地的media路径映射为本地文件path'''
    path = os.path.join( os.path.dirname(settings.BASE_DIR),url[1:] )
    return path