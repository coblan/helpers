from helpers.director.shortcut import TablePage,ModelTable,ModelFields,page_dc,RowFilter,director
from .models import GeneralLog

class GeneralLogPage(TablePage):
    def get_label(self):
        return '普通日志'
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(ModelTable):
        model = GeneralLog
        exclude =['id']
        pop_edit_fields = ['createtime']
        selectable = False
        
        def get_operation(self):
            return []
        
        def dict_head(self, head):
            width = {
                'message':400,
                'createtime':180,
            }
            if head['name'] in width:
                head['width'] = width.get(head['name'])
            return head
        
        def dict_row(self, inst):
            return {
                'createtime':inst.createtime.strftime('%y-%m-%d %H:%M:%S.%f')
            }
        
        class filters(RowFilter):
            names =['message','level','process',]
            icontains = ['message','level','process',]
            range_fields = ['createtime']

class GeneralLogForm(ModelFields):
    class Meta:
        model = GeneralLog
        exclude =[]
        
    def dict_head(self, head):
        head['readonly'] = True
        return head

director.update({
    'general_log':GeneralLogPage.tableCls,
    'general_log.edit':GeneralLogForm
})

page_dc.update({
    'general_log':GeneralLogPage
})