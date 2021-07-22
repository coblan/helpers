from helpers.director.shortcut import TablePage,ModelTable,ModelFields,page_dc,director,director_view,RowFilter
from .models import SystemMessage

class SystemMessagePage(TablePage):
    def get_label(self):
        return '系统消息'
    def get_template(self, prefer=None):
        return 'jb_admin/table_new.html'
    
    class tableCls(ModelTable):
        model = SystemMessage
        exclude =[]
        
        def get_operations(self):
            ops = [] # super().get_operations()
            ops += [
                {
                    'name':'has_read',
                    'label':'已读',
                    'editor':'com-btn',
                    'disabled_express':'rt = scope.ps.selected.length == 0',
                    'preset_express':'rt={read:true}',
                    'click_express':'scope.ps.selected_set_and_save(scope.head)',
                    },
                {'name':'all_read',
                 'label':'全部已读',
                 'editor':'com-btn',
                 'click_express':'cfg.show_load();ex.director_call("act_log.system_message.all_read",{}).then(()=>{cfg.hide_load(2000);scope.ps.search()})'}
            ]
            return ops
        
        class filters(RowFilter):
            names = ['read','level']
            range_fields=['createtime']


class SystemMessageForm(ModelFields):
    class Meta:
        model = SystemMessage
        exclude =[]

@director_view('act_log.system_message.all_read')
def system_message_all_read():
    SystemMessage.objects.filter(read=False).update(read=True)

director.update({
    'system_message':SystemMessagePage.tableCls,
    'system_message.edit':SystemMessageForm,
})

page_dc.update({
    'system_message':SystemMessagePage
})