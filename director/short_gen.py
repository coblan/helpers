from .model_admin.fields import ModelFields
from .model_admin.tabel import ModelTable
from .pages import FormPage,TablePage
from .model_admin.base import model_dc,permit_list,page_dc

def regist_director(prefix_list,src_model):
    class ThisForm(ModelFields):
        class Meta:
            model=src_model
            exclude=[]
    class ThisFormPage(FormPage):
        fieldsCls=ThisForm
    
    class ThisTable(ModelTable):
        model=src_model
        exclude=[]
    
    class ThisTablePage(TablePage):
        tableCls=ThisTable
    
    dc={}
    for prefix in prefix_list:
        dc[prefix]=ThisTablePage
        dc[prefix+'.edit']=ThisFormPage
    
    model_dc[src_model]={'fields':ThisForm}
    permit_list.append(src_model)
    page_dc.update(dc)
    return dc
