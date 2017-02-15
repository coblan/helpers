# encoding:utf-8
from __future__ import unicode_literals

from helpers.director import model_dc,model_page_dc,TablePage,ModelTable,FormPage
from models import WebPage
from base import web_page_templates

class WebPageTable(ModelTable):
    model = WebPage
    include=['name','label','temp','status']    

class WebPageTablePage(TablePage):
    tableCls=WebPageTable

class WebPageForm(ModelFields):
    class Meta:
        model=WebPage
        fields=['name','label','temp','status','text']
    
    def get_heads(self):
        heads=super(WebPageForm,self).get_heads()
        for head in list(heads):
            if head['name']=='temp':
                head['type']='sim_select'
                
                head['options']=[{'value':x,'label':x} for x in web_page_templates]
            if head['name']=='status':
                head['type']='sim_select'
                head['options']=[
                    {'value':'active','label':'Active'},
                    {'value':'deactive','label':'Deactive'}
                ]
                head['default']='deactive'
            if head['name']=='text':
                heads.remove(head)
                
        return heads

class WebPageFormPage(FormPage):
    fieldsCls=PageForm
    template='page_adapt/page_form.html'


model_dc[WebPage]={'fields':PageForm}
model_page_dc['webpage']={'table':WebPageTablePage,'form':WebPageFormPage}