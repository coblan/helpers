# encoding:utf-8
from __future__ import unicode_literals
import time
import inspect

class TablePage(object):
    template=''
    tableCls=''
    extra_js=[]
    def __init__(self,request, engin):
        if request.GET.get('_accept')=='json' or 'json' in request.META.get('HTTP_ACCEPT'):
            self.accept = 'json'
        else:
            self.accept = ''
            
        self.engin = engin
        if not self.tableCls:
            for k,v in self.__class__.__dict__.items():
                if inspect.isclass(v) and issubclass(v,ModelTable):
                    self.tableCls = v
                    break
        
        self.request=request
        self.table = self.tableCls.parse_request(request)
        self.crt_user=request.user
        #self.permit=self.table.permit #ModelPermit(self.table.model,self.crt_user)
    
    def get_template(self,prefer=None):
        if self.template:
            return self.template
        elif prefer=='f7':
            return 'f7/table.html'
        else:
            return 'director/table.html'
    
    def get_context(self):
        """
        _empty_data:是为了返回没有数据的页面，当作模版用，在framework7的优化过程中，产生了这个需求。但是没有成功，所以这个_empty_data可能没用。
        """
        
        if self.accept =='json':
            ctx=self.table.get_data_context()
        else:
            ctx = self.table.get_context()
            ctx['extra_js'] = list( self.extra_js )
        #ctx['can_add']=self.permit.can_add()
        #ctx['can_del']=self.permit.can_del()
        #if self.permit.changeable_fields:
            #ctx['can_edit']=True
        #ctx['app']=self.tableCls.model._meta.app_label
        # ctx['page_label'] =self.get_label()
       
        return ctx
    
    def get_label(self):
        """
        返回空，让title默认显示菜单项的名字
        """
        return getattr(self,'page_label',' ')
    

