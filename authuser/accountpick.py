from helpers.director.shortcut import ModelTable,RowFilter,director
from django.contrib.auth.models import User

class AccountPicker(ModelTable):
    model = User
    exclude = []
    fields_sort=['id','username','first_name']
    def dict_head(self, head):
        width = {
            'username':160,
            'first_name':230
        }
        if head['name'] in width:
            head['width'] = width[head['name']]
        if head['name'] =='username':
            head['editor'] = 'com-table-foreign-click-select'
        return head
    
    class filters(RowFilter):
        names=['username','first_name']
        icontains = ['username','first_name']
        

director.update({
    'AccountPicker':AccountPicker
})