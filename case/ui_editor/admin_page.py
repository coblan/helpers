from helpers.director.shortcut import TablePage,ModelTable,ModelFields,page_dc,director,get_request_cache,director_view,RowSort
from . models import Page
import json
from django.conf import settings
import os
from helpers.director.kv import get_json,set_json
import sys

def check_and_import():
    page_json_path = os.path.join(settings. BASE_DIR, 'static','page.json').replace('\\', '/')
    tm =  os.path.getmtime(page_json_path)
    if tm > get_json('_page_json_modify_time',0):
        print('更新uie组件到page.json')
        import_ui_editor_data()
        set_json('_page_json_modify_time',tm)


class PagePage(TablePage):
    def get_label(self):
        return '页面管理'
    
    def get_template(self, prefer=None):
        return 'jb_admin/table_new.html'
    
    class tableCls(ModelTable):
        model = Page
        exclude =[]
        #pop_edit_fields =['name']
        hide_fields =['content']
        button_edit = True
        allow_delete= True
        
        def get_head_context(self):  
            get_request_cache()['named_ctx'].update({
                          'order-page-tabs':[
                              {'name':'uitest',
                              'label':'ui测试',
                               'editor':'com-tab-ui-editor',
                             
                               },
         
                          ]
                      })   
            ctx = super().get_head_context()
            return ctx
        
        #def get_operations(self):
            #ops = super().get_operations()
            #ops+= [{
                #'editor':'com-btn',
                #'label':'固化',
                #'click_express':'''cfg.confirm("确定保存并覆盖以前的数据?").then(()=>{
                    #cfg.show_load();
                    #return ex.director_call("save_ui_editor_data")
                #}).then(()=>{cfg.hide_load();cfg.toast("操作成功")})'''
                
            #},{
                #'editor':'com-btn',
                #'label':'导入',
                #'click_express':''' cfg.confirm("确定要导入页面?").then(()=>{
                    #cfg.show_load();
                    #return ex.director_call("import_ui_editor_data")
                #}).then(()=>{cfg.hide_load();cfg.toast("操作成功")}) 
                #'''
            #}]
            #return ops
        
        def dict_head(self, head):
            width = {
                'name':300
            }
            head['width'] = width.get(head['name'])
            if head['name']=='name':
                head['editor'] = 'com-table-click'
                head['click_express']="scope.ps.switch_to_tab({ctx_name:'order-page-tabs',tab_name:'uitest',par_row:scope.row})"
            return head
        
        class sort(RowSort):
            names=['sort']
            general_sort ='sort'
        



@director_view('save_ui_editor_data')
def save_ui_editor_data():
    rows =[]
    for inst in Page.objects.all():
        rows.append({
            'name':inst.name,
            'desp':inst.desp,
            'sort':inst.sort,
            'content':inst.content
        })
    with open( os.path.join( settings.STATICFILES_DIRS[0],'page.json'),'w',encoding='utf-8' ) as f:
        json.dump(rows,f)

@director_view('import_ui_editor_data')
def import_ui_editor_data():
    page_json_path = os.path.join(settings. BASE_DIR, 'static','page.json').replace('\\', '/')
    with open( page_json_path,'r',encoding='utf-8' ) as f:
        rows = json.load(f)   
    for row in rows:
        Page.objects.update_or_create(name=row.get('name'),defaults={ 'desp':row.get('desp','') ,
                                                                      'sort':row.get('sort',0),
                                                                      'content':row.get('content')})
              

class PageForm(ModelFields):
    class Meta:
        model = Page
        exclude =[]
    
    def dict_head(self, head):
        if head['name'] == 'content':
            head['editor'] = 'com-field-json-edit'
        return head
    
    def after_save(self):
        save_ui_editor_data()

@director_view('uie/page')
def uie_page(name):
    inst = Page.objects.get(name=name)
    return json.loads(inst.content)

if 'collectstatic' in sys.argv:
    check_and_import()


director.update({
    'webpage':PagePage.tableCls,
    'webpage.edit':PageForm
})

page_dc.update({
    'webpage':PagePage
})