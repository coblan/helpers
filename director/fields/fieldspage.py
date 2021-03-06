# encoding:utf-8
from __future__ import unicode_literals

class FieldsPage(object):
    template=''
    fieldsCls=''
    ajax_scope={}
    extra_js=[]
    ex_css=[]
    def __init__(self,request, engin):
        self.engin = engin
        #if not self.fieldsCls:
            #for k,v in self.__class__.__dict__.items():
                #if inspect.isclass(v) and issubclass(v,ModelFields):
                    #self.fieldsCls = v
                    #break            
        
        self.request=request
        #self.pk=request.GET.get('pk')
        if self.fieldsCls:
            self.fields = self.fieldsCls.parse_request(request) # (pk=self.pk,crt_user=request.user,request=request)

        
    
    def get_template(self,prefer=None): 
        if self.template:
            return self.template
        elif prefer=='f7':
            return 'f7/fields.html'
        else:
            return 'director/fields.html'
    
    def get_context(self):
        self.ctx={}
        if self.fieldsCls:
            dc = self.fields.get_context()
            self.ctx.update(dc)
            self.ctx['fields_ctx'] = dc
            
        self.ctx['extra_js']=self.extra_js
        self.ctx['ex_css'] = self.ex_css        
        
        # self.ctx['page_label'] =self.get_label()
        return self.ctx
    
    def get_label(self):
        
        return  '' #str(self.fields.instance)  #'编辑表单'  
    
