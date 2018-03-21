from django.contrib import admin

# Register your models here.
import cgi

class KVTable(ModelTable):
    model=KVModel
    exclude=[]
    def dict_row(self, inst):
        if len(inst.value)>50:
            value=inst.value[:50]+'...'
        else:
            value=inst.value
        return {
            'value':cgi.escape(value)
        }

class KvTablePage(TablePage):
    tableCls=KVTable

class KvFields(ModelFields):
    class Meta:
        model=KVModel
        exclude=[]

class KvFormPage(FieldsPage):
    fieldsCls=KvFields
    def get_template(self, prefer=None):
        if prefer=='wx':
            return 'wx/kvform.html'
        else:
            return 'director/kvform.html'

# short_gen.regist_director(['kv','kv.wx'],KVModel)
page_dc.update({
    'kv':KvTablePage,
    'kv.edit':KvFormPage,
})

model_dc[KVModel]={'fields':KvFields}