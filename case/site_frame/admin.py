# encoding:utf-8
from __future__ import unicode_literals
from __future__ import absolute_import
from helpers.director.shortcut import page_dc
from helpers.director import kv


class MHome(object):
    template='wx/home.html'
    need_login=False
    def __init__(self,request):
        self.request=request
    
    def get_context(self):
        return {}


class F7Home(object):
    template='f7/home.html'
    need_login=False
    ajax_html=True
    def __init__(self,request):
        self.request=request
    
    def get_context(self):
        return {}  

class F7HomeWraper(F7Home):
    template='f7/home_wraper.html'

    
class Help(object):
    template='site_frame/help_f7.html'
    def __init__(self,request):
        self.request=request
        
    def get_context(self):
        ctx={
            'help_text':kv.get_value('help_text','')
        }        
        return ctx


page_dc.update({
    'home.wx':MHome,
    'home.f7':F7HomeWraper,
    'home_real.f7':F7Home,
    'help.f7':Help,
})