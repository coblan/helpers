# encoding:utf-8
"""
在总的urls.py文件的底部，调用common_urls()获得补全的urls
from this_file import *
"""
from __future__ import unicode_literals
from django.conf import settings
from django.conf.urls.static import static
from helpers.director import views as director_views
from helpers.director.ex_interface import rec_file

def common_urls():
    urlpatterns = [
        
        url(r'^_ajax/(?P<app>\w+)?/?$',director_views.ajax_views,name='ajax_url'),
        url(r'^_ajax/?$',director_views.ajax_views), 
        url(r'^_face/', include(face_urls)),
        url(r'^_download/(?P<app>\w+)?/?$',director_views.donwload_views,name='download_url'), 
        url(r'^upload/?$',rec_file.general),
    ]

    if settings.DEBUG:
        urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    return urlpatterns