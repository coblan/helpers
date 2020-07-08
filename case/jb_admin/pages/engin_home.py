from helpers.director.shortcut import page_dc

class EngineHome(object):
    def __init__(self, request,engin):
        self.request = request
        self.engin = engin
    
    def get_label(self):
        return '首页'
    
    def get_template(self):
        return 'jb_admin/live.html'
    
    def get_context(self):
        return {
            'editor':'com-engin-home',
            'editor_ctx':{
                'title':self.engin.title
            }
        }

page_dc.update({
    'enginhome':EngineHome
})