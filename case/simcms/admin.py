from django.contrib import admin
from helpers.director.shortcut import TablePage, ModelTable, ModelFields, page_dc, director
from .models import CmsPageModel
from .base_data import cms_page
from helpers.maintenance.update_static_timestamp import js_stamp_dc

# Register your models here.
class CmsTablePage(TablePage):
    template = 'jb_admin/table.html'
    extra_js=['/static/js/simcms.pack.js?t=%s'%js_stamp_dc.get('simcms_pack_js','')]
    def get_label(self): 
        return '页面编辑'
    
    class tableCls(ModelTable):
        model = CmsPageModel
        exclude = []
        hide_fields = ['id']
        pop_edit_field = 'name'
        
        def dict_head(self, head): 
            if head['name'] == 'content':
                head['editor'] = 'com-table-extraclick'
                head['extra_label'] = '编辑'
                head['extra_fun'] = 'edit_page_content'
                #head['editor'] = 'com-table-pop-fields'
                #head['show_label'] = {
                    #'fun': 'text_label',
                    #'text': '编辑',
                #}
                #head['fields_ctx'] = CmsForm(crt_user= self.crt_user).get_head_context()
                #head['after_save']={
                    #'fun':'update_or_insert'
                #}              
                #head['get_row']={
                    #"fun":'use_table_row', 
                #}                  
                
            return head
        
        def get_context(self): 
            ctx = super().get_context()
            ctx['extra_table_logic'] = 'simcms_table_logic'
            return ctx
        
        #def dict_row(self, inst): 
            #return {
                #'_fields_ctx' : {
                    #'heads': cms_page[inst.temp_cls].getHeads(),
                    #'ops': [],
                    
            #}
                

class CmsForm(ModelFields):
    hide_fields = ['content']
    class Meta:
        model = CmsPageModel
        exclude = []
    
    def dict_head(self, head): 
        if head['name'] == 'temp_cls':
            head['editor'] = 'sim_select'
        return head
    
    def dict_options(self): 
        return {
            'temp_cls': [{'value': k, 'label': k,}for k, v in cms_page.items()],
        }

    
    
director.update({
    'simcms.page': CmsTablePage.tableCls,
    'simcms.page.edit':CmsForm
})

page_dc.update({
    'simcms.page': CmsTablePage,
})
