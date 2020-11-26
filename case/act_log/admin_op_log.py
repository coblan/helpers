from helpers.director.shortcut import TablePage,ModelTable,ModelFields,page_dc,director,RowFilter
from .models import BackendOperation
from django.conf import settings

class BackendOperationPage(TablePage):
    def get_label(self):
        return '操作日志'
    
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(ModelTable):
        model = BackendOperation
        exclude =['id']
        pop_edit_fields = ['createtime']
        selectable = False
        
        def get_operation(self):
            return []
        
        def dict_head(self, head):
            width = {
                'model':150,
                'content':600,
                 'createtime':180,
            }
            if head['name'] in width:
                head['width'] = width[head['name']]
            return head
        
        def dict_row(self, inst):
            return {
                'createtime':inst.createtime.strftime('%Y-%m-%d %H:%M:%S.%f')
            }
        
        class filters(RowFilter):
            names = ['model','inst_pk','content','createuser']
            icontains = ['model','content','createuser']
            range_fields = ['createtime']
            
            def dict_head(self, head):
                if head['name'] == 'inst_pk':
                    head['editor'] = 'com-filter-exact-text'
                    head['options'] =[]
                return head
            def clean_search_args(self, search_args):
                if search_args.get('content'):
                    if getattr(settings,'DB_FULL_SEARCH',False):
                        search_args['content__search'] = search_args.pop('content')
                return search_args            
            
            

class BackendOperationForm(ModelFields):
    class Meta:
        model = BackendOperation
        exclude = []
    
    def dict_head(self, head):
        head['readonly'] = True
        return head

director.update({
    'backendoperation_log':BackendOperationPage.tableCls,
    'backendoperation_log.edit':BackendOperationForm
})

page_dc.update({
    'backendoperation_log':BackendOperationPage
})