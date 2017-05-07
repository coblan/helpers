from .model_admin.fields import ModelFields
from .model_admin.tabel import ModelTable
from .pages import FormPage,TablePage

def dict_for_engine(prefix_list,model):
    class ThisForm(ModelFields):
        class Meta:
            model=model
            exclude=[]
    class ThisFormPage(FormPage):
        fieldsCls=ThisForm
    
    class ThisTable(ModelTable):
        model=model
        exclude=[]
    
    class ThisTablePage(TablePage):
        tableCls=ThisTable
    
    dc={}
    for prefix in prefix_list:
        dc[prefix]=ThisTablePage
        dc[prefix+'.edit']=ThisFormPage
    
    return dc
