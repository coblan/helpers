# encoding:utf-8
"""
由于director模块采用了没有前缀的url，所以只能用函数去改造urlpatterns,
详细见direcotr.ex_setting.put_in_urls

#"""
from __future__ import unicode_literals
from django.conf.urls import include, url
from . import views
from .network import rec_file
from . import qr

#def common_urls():
    #urlpatterns = [
        
        #url(r'^_ajax/(?P<app>\w+)?/?$',director_views.ajax_views,name='ajax_url'),
        #url(r'^_ajax/?$',director_views.ajax_views), 
        #url(r'^_face/', include(face_urls)),
        #url(r'^_download/(?P<app>\w+)?/?$',director_views.donwload_views,name='download_url'), 
        #url(r'^upload/?$',rec_file.general),
    #]


    
    #return urlpatterns


urlpatterns = [
    url(r'^ajax/(?P<app>\w+)?/?$',views.ajax_views,name='ajax_url'),
    url(r'^ajax/?$',views.ajax_views), 
    url(r'^upload/?$',views.general_upload,name='general_upload'), #,rec_file.general)
    url(r'^ckeditor_image', views.ckeditor, name= 'ckeditor_upload_image'), 
    url(r'^excel/?$', views.export_excel), 
    url(r'^qr/?$',qr.general_qr),
    url(r'^helloworld',views.helloworld)
]