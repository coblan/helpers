from helpers.director.shortcut import page_dc
from . models import Page
import json
from helpers.pcweb.shotcut import web_page_dc

#def uie_backend_page(text):
    #pass

class WebPage(object):
    def __init__(self, request,*args, **kwargs):
        self.request = request
    
    def get_template(self):
        return 'director/vuebase.html'
    
    def get_context(self):
        pagename = self.request.GET.get('uie')
        inst = Page.objects.get(name=pagename)
        return {
            'editor':'uie-mount-view',
            'editor_ctx':{
                'heads':json.loads(inst.content)
                #'tableCtx':{ 'autoHeight':True,'opMergeCount':3, **DeviceTable().get_head_context()}
            }
        }

web_page_dc.update({
    'uie':WebPage
})