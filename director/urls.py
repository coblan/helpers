# encoding:utf-8

from django.conf.urls import include, url
import views

from model_admin import render
"""
为了简短的url，这个路由直接放到总的urls.py里面去了

    url(r'^ajax/(?P<app>\w+)?/?$',director_views.ajax_views,name='ajax_url'),
    url(r'^ajax/?$',director_views.ajax_views),

"""
urlpatterns = [
    #url(r'^login/?$',views.login,name='login'),
    #url(r'^regist/?$',views.regist_user,name='regist'),
    #url(r'^logout/?$',views.logout),
    #url(r'^pswd/?$',views.change_pswd),
    
    #url(r'^ajax/(?P<app>\w+)/?$',views.ajax_views,name='ajax_url'),
    
    #url(r'^$',views.trival,name='director'),
    #url(r'^model/(?P<name>\w+)/edit/?$',render.form_view,name='model_new'),
    #url(r'^model/(?P<name>[^\/]+)/edit/(?P<pk>[^\/]+)/?$',render.form_view,name='model_edit'),
    #url(r'^model/(?P<name>\w+)/history/(?P<pk>\w+)/?$',render.form_history,name='model_history'),
    #url(r'^model/(?P<name>\w+)/$',render.table_view,name='model_table'),
    #url(r'^del_rows/?$',render.del_rows,name='del_rows'),
    
]