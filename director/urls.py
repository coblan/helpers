# encoding:utf-8

from django.conf.urls import include, url

"""
由于director模块采用了没有前缀的url，所以只能用函数去改造urlpatterns,
详细见direcotr.ex_setting.put_in_urls

#"""
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


    
    return urlpatterns


urlpatterns = [
    url(r'^ajax/(?P<app>\w+)?/?$',director_views.ajax_views,name='ajax_url'),
    url(r'^ajax/?$',director_views.ajax_views), 
    url(r'^face/', include(face_urls)),
    url(r'^download/(?P<app>\w+)?/?$',director_views.donwload_views,name='download_url'), 
    url(r'^upload/?$',rec_file.general),    
]