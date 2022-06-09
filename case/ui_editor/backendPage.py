from helpers.director.shortcut import page_dc
from . models import Page
import json

#def uie_backend_page(text):
    #pass

class BackendPage(object):
    def __init__(self, request,*args, **kwargs):
        self.request = request
    
    def get_template(self):
        return 'jb_admin/live.html'
    
    def get_context(self):
        pagename = self.request.GET.get('uie')
        inst = Page.objects.get(name=pagename)
        return {
            #'editor':'com-live-devcieAdmin',
            'editor':'uie-mount-view',
            'editor_ctx':{
                'heads':json.loads(inst.content)
                #'tableCtx':{ 'autoHeight':True,'opMergeCount':3, **DeviceTable().get_head_context()}
            }
        }

page_dc.update({
    'uie_backend_page':BackendPage
})