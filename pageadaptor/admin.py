# encoding:utf-8
from __future__ import unicode_literals

from helpers.director.shortcut import model_dc,model_page_dc,TablePage,ModelTable,FormPage,ModelFields
from models import WebPage
from stencil import web_page_templates
from pydoc import locate
from django.conf import settings

dir_engine=locate(settings.DIR_ENGINE)

class WebPageTable(ModelTable):
    model = WebPage
    include=['name','label','temp','status']    

class WebPageTablePage(TablePage):
    tableCls=WebPageTable

class WebPageForm(ModelFields):
    class Meta:
        model=WebPage
        fields=['name','label','temp','status','content']
    
    def get_heads(self):
        heads=super(WebPageForm,self).get_heads()
        for head in list(heads):
            if head['name']=='temp':
                head['type']='sim_select' 
                head['options']=web_page_templates
            if head['name']=='status':
                head['type']='sim_select'
                head['options']=[
                    {'value':'active','label':'Active'},
                    {'value':'deactive','label':'Deactive'}
                ]
                head['default']='deactive'
            if head['name']=='content':
                heads.remove(head)
                
        return heads

class WebPageFormPage(FormPage):
    fieldsCls=WebPageForm
    template='pageadaptor/page_form.html'


model_dc[WebPage]={'fields':WebPageForm}
# model_page_dc['webpage']={'table':WebPageTablePage,'form':WebPageFormPage}
dir_engine.add_pages({
    'webpage':WebPageTablePage,
    'webpage.edit':WebPageFormPage,
})