from .table import ModelTable,director
from django.db.models import Count,F,OuterRef, Subquery,Exists

class TreeTable(ModelTable):
    first_field=''
    selectable = False
    def inn_filter(self, query):
        if self.kw.get('par'):
            query  =query.filter(parent_id = self.kw.get('par'))
        else:
            query = query.filter(parent__isnull = True)
        subquery = self.model.objects.filter(parent=OuterRef('pk'))
        query = query.annotate(hasChildren=Exists(subquery))
        return query
    
    def getExtraHead(self):
        model_form = director.get(self.get_edit_director_name())
        if model_form:
            return [
                {'name':'op','label':'操作','editor':'com-table-ops-cell',
                 'ops':[
                      {'editor':'com-btn', 
                       'label':'创建',
                       'width':100,
                       #'icon':'el-icon-phone',
                       #'fa_icon':'fa fa-phone-square',
                       'type':'primary',
                       'css':'.myphone button{ padding: 2px;}',
                       'class':'myphone',
                       'fields_ctx':model_form().get_head_context(),
                       'click_express':"scope.head.fields_ctx.preset={parent:scope.ps.vc.rowData.pk}; cfg.pop_vue_com('com-form-one',scope.head.fields_ctx).then(()=>{ scope.ps.vc.rowData.hasChildren=true;scope.ps.vc.parStore.vc.$refs.dtable.updateNode( scope.ps.vc.rowData) })"},
                      {'editor':'com-btn',
                       'label':'删除',
                       'width':100,
                       'type':'warning',
                       'class':'myphone',
                       'click_express':'''
                       cfg.show_load();
                       ex.director_call("d.delete_query_related",{rows:[scope.ps.vc.rowData]}).then((resp)=>{
                     cfg.hide_load();
                     if(resp.length>0){
                         cfg.pop_vue_com("com-pan-delete-query-message",{msg_list:resp,genStore:scope.ps,title:"删除关联确认"})
                     }else{
                        cfg.confirm("确认删除?").then(()=>{
                            cfg.show_load()
                            return ex.director_call('d.delete_rows',{rows:[scope.ps.vc.rowData]})
                          }).then(()=>{
                            cfg.hide_load()
                            if(scope.ps.vc.rowData.parent){
                                scope.ps.vc.parStore.vc.$refs.dtable.updateNode( {pk:scope.ps.vc.rowData.parent})
                            }else{
                                scope.ps.vc.parStore.vc.search()
                            }
                            
                          })
                        
                     }
                    
                 });''',
                       },
                      {'editor':'com-btn-drop',
                       'label':'更多',
                       'class':'myphone',
                       'menu':[
                           {'label':'剪切','click_express':'var row=scope.ps.vc.rowData;window.cut_data=row;cfg.toast("剪切成功")'},
                           {'label':'粘贴','click_express':'''
                           var row = window.cut_data;
                           var old_parent_pk = row.parent
                           var new_parent=scope.ps.vc.rowData;
                           row.parent=new_parent.pk; 
                           ex.director_call('d.save_row',{row:row}).then(()=>{
                               scope.ps.vc.parStore.vc.$refs.dtable.updateNode( {pk:old_parent_pk})
                               new_parent.hasChildren=true
                               scope.ps.vc.parStore.vc.$refs.dtable.updateNode( {pk:new_parent.pk})
                           })''' },
                           {'label':'移到顶层',
                            'click_express':'''
                            var row=scope.ps.vc.rowData;
                            var old_parent_pk = row.parent
                            row.parent=null;
                            ex.director_call('d.save_row',{row:row}).then(()=>{
                               scope.ps.vc.parStore.vc.$refs.dtable.updateNode( {pk:old_parent_pk})
                               scope.ps.vc.parStore.vc.search()
                           })
                            '''}
                           ]
                           }
                     ]}
                ]
        else:
            return []
    
    def dict_head(self, head):
        width = {
            self.first_field:200,
            'op':150,
        }
        head['width'] = width.get(head['name'])
        if head['name']==self.first_field:
            head['class']='chuizhi'
            head['css']='''.chuizhi:first-child{margin-left:23px}'''
        return head    
    
    def dict_row(self, inst):
        return {
            'hasChildren':inst.hasChildren,               
        }    