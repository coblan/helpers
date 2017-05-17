# encoding:utf-8

from __future__ import unicode_literals
import requests
from django.shortcuts import redirect
import json
from django.contrib.auth.models import User
from django.contrib import auth 
from .models import WxInfo
import urllib

class FuWuHao(object):
    """
    先重定向，获取到code
    再调用code获取token和openid，
    如果是第一次登陆，会再利用token获取用户信息，并且保存下来。
    """
    APPID='wx7080c32bd10defb0'
    APPSECRET='d4624c36b6795d1d99dcf0547af5443d'
    WxInfo=WxInfo
    scheme='http'
    def get_redirect_url(self,request):
        host=request.META['HTTP_HOST']
        red_url=self.scheme+'://'+host+'/_wechat/rec_code'
        red_url=urllib.quote(red_url)
        url="https://open.weixin.qq.com/connect/oauth2/authorize?appid=%(appid)s&redirect_uri=%(redirect_url)s&response_type=code&scope=%(scope)s&state=123#wechat_redirect"\
            %{'appid':self.APPID,'redirect_url':red_url,'scope':'snsapi_userinfo'}
        return url
    
    def rec_code(self,request):
        code=request.GET.get('code')
        print('code is %s'%code)
        url='https://api.weixin.qq.com/sns/oauth2/access_token?appid=%(appid)s&secret=%(secret)s&code=%(code)s&grant_type=authorization_code'\
            %{'appid':self.APPID,'secret':self.APPSECRET,'code':code}
        resp=requests.get(url)
        dc = json.loads(resp.content)
        openid = dc['openid']
        token=dc['access_token']
        wxuser,c = WxInfo.objects.get_or_create(openid=openid)
        print('save ok')
        if c:
            dc = self.get_info(token,openid)
            wxuser.head=dc['headimgurl']
            wxuser.sex=dc['sex']
            wxuser.nickname=dc['nickname']
            wxuser.province=dc['province']
            wxuser.city=dc['city']
            wxuser.country=dc['country']
            wxuser.save()
            
        self.on_login(request,wxuser)
        
    
    def get_info(self,token,openid):
        url='https://api.weixin.qq.com/sns/userinfo?access_token=%(access_token)s&openid=%(openid)s&lang=zh_CN'\
            %{'access_token':token,'openid':openid}
        resp=requests.get(url)
        return json.loads(resp.content)

    def on_login(self,request,wxuser):
        if not wxuser.user:
            wxuser.user=User.objects.create()
            wxuser.save()
        auth.login(request, wxuser.user)
        print('log in ok')
        

if __name__=='__main__':
    o=FuWuHao()
    