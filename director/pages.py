

class TablePage(object):
    template='director/table.html'
    tableCls=''
    ajax_scope={}
    def __init__(self,request):
        self.request=request
        self.table = self.tableCls.parse_request(request)
        self.crt_user=request.user
       
    def get_context(self):
        ctx = self.table.get_context()
        #pop = self.request.GET.get('_pop')
        #if not pop:
            #menu_list=list( render_dc.get('menu') )
            #ctx['menu']=evalue_container(menu_list,user=self.request.user)        

        return ctx
    
class FormPage(object):
    template='director/fields.html'
    fieldsCls=''
    ajax_scope={}
    def __init__(self,request):
        self.request=request
        self.pk=request.GET.get('pk')
        self.fields = self.fieldsCls(pk=self.pk,crt_user=request.user)
        
    def get_context(self):
        ctx = self.fields.get_context()
        #pop = self.request.GET.get('_pop')
        #if not pop:
            #ctx['menu']=evalue_container(render_dc.get('menu'),user=self.request.user)  
        return ctx