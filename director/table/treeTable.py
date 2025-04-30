from .table import ModelTable,director,RowSort,PageNum
from django.db.models import Count,F,OuterRef, Subquery,Exists

class TreeTable(ModelTable):
    first_field=''
    selectable = False
    parent_null= None
    
    class pagenator(PageNum):
        def __init__(self, pageNumber=1, perpage=None, **kws):
            super().__init__(pageNumber, perpage, **kws)
            self.table = kws.get('table')
            
        def get_slice_index(self):
            if self.table.kw.get('search_args').get('par'):
                return 0,1000
            else:
                return super().get_slice_index()
    
    class sort(RowSort):
        general_sort ='pk'
    
    def getRootQuery(self,query):
        return None
    
    def inn_filter(self, query):
        if self.kw.get('par'):
            query  =query.filter(parent_id = self.kw.get('par'))
        else:
            root_query = self.getRootQuery(query)
            if root_query:
                query = root_query
            elif self.parent_null != None:
                query = query.filter(parent_id = self.parent_null)
            else:
                query = query.filter(parent__isnull = True)
        self.count_query = query
        subquery = self.model.objects.filter(parent=OuterRef('pk'))
        query = query.annotate(hasChildren=Exists(subquery))
        
        return query
    
    def get_operations(self):
        ops = super().get_operations()
        for op in ops:
            if op['name']=='add_new':
                op['click_express']='''scope.head.fields_ctx.genVc=scope.vc;
                scope.ps.add_new(scope.head).then(()=>{
                    scope.ps.search()
                })
                 
                '''
        return ops
    
    def getExtraHead(self):
        model_form = director.get(self.get_edit_director_name())
        if model_form and self.permit.can_edit():
            return [
                {'name':'op',
                 'label':'操作',
                 'editor':'com-table-ops-cell',
                 'ops':[
                      {'editor':'com-btn', 
                       'label':'创建下级',
                       
                       #'icon':'el-icon-phone',
                       #'fa_icon':'fa fa-phone-square',
                       'type':'primary',
                       'css':'.myphone button{ padding: 2px;}',
                       'class':'myphone',
                       'fields_ctx':model_form().get_head_context(),
                       #'click_express':"scope.head.fields_ctx.preset={parent:scope.ps.vc.rowData.pk}; cfg.pop_vue_com('com-form-one',scope.head.fields_ctx).then(()=>{ scope.ps.vc.rowData.hasChildren=true;scope.ps.vc.parStore.vc.$refs.dtable.updateNode( scope.ps.vc.rowData) })"
                        'click_express':'''cfg.show_load(); ex.director_call('d.get_row',{director_name:scope.head.fields_ctx.director_name,parent:scope.ps.vc.rowData.pk}).then((row)=>{
                            cfg.hide_load()
                            row.parent = scope.ps.vc.rowData.pk
                            scope.head.fields_ctx.row=row
                            return cfg.pop_vue_com('com-form-one',scope.head.fields_ctx)
                        }) .then(()=>{ 
                            Vue.set(scope.ps.vc.rowData,'hasChildren',true);
                            scope.ps.vc.parStore.vc.$refs.dtable.updateNode( scope.ps.vc.rowData) 
                        })''' 
                        
                       },
                      {'editor':'com-btn',
                       'label':'删除',
                       'width':100,
                       'type':'warning',
                       'class':'myphone',
                       'visible':self.permit.can_del(),
                       'click_express':''' 
                       var func = async ()=>{
                                 cfg.show_load();
                                 var resp = await ex.director_call("d.delete_query_related",{rows:[scope.ps.vc.rowData]})
                                 cfg.hide_load();
                                 if(resp.length>0){
                                    var resp2 = await cfg.pop_vue_com("com-pan-delete-query-message",{msg_list:resp,title:"删除关联确认"})
                                    if(!resp2){
                                        return
                                    }
                                 }else{
                                    await cfg.confirm("确认删除?")
                                 }
                                cfg.show_load()
                                await ex.director_call('d.delete_rows',{rows:[scope.ps.vc.rowData]})
                                cfg.hide_load()
                                if(scope.ps.vc.rowData.parent){
                                    scope.ps.vc.parStore.vc.$refs.dtable.updateNode( {pk:scope.ps.vc.rowData.parent})
                                }else{
                                    scope.ps.vc.parStore.vc.search()
                                }
                       }
                       func()
                      ''',
                       },
                      {'editor':'com-btn-drop',
                       'label':'更多',
                       'class':'myphone',
                       'menu':[
                           {'label':'剪切','click_express':'var row=scope.ps.vc.rowData;window.cut_data=row;cfg.toast("剪切成功")'},
                           {'label':'粘贴','click_express':'''( async ()=>{
                               if(!window.cut_data){
                                    cfg.toast("先执行剪切操作,才能粘贴")
                                    return
                               }
                                var row = window.cut_data;
                                var old_parent_pk = row.parent
                                var new_parent=scope.ps.vc.rowData;
                                if(row.pk == new_parent.pk){
                                    cfg.toast("不能选择自己作为自己的上级")
                                    return
                                }
                                row.parent=new_parent.pk; 
                                var resp = await ex.director_call('d.save_row',{row:row})
                                 scope.ps.vc.parStore.vc.$refs.dtable.updateNode( {pk:old_parent_pk})
                                 new_parent.hasChildren=true
                                 scope.ps.vc.parStore.vc.$refs.dtable.updateNode( {pk:new_parent.pk})
                                 window.cut_data =null
                           })()''' },
                           {'label':'移到顶层',
                            'click_express':'''
                            var row=scope.ps.vc.rowData;
                            var old_parent_pk = row.parent
                            row.parent=%s;
                            ex.director_call('d.save_row',{row:row}).then(()=>{
                               scope.ps.vc.parStore.vc.$refs.dtable.updateNode( {pk:old_parent_pk})
                               scope.ps.vc.parStore.vc.search()
                           })
                            '''%( 'null' if self.parent_null==None else self.parent_null)  }
                           ]
                           }
                     ]}
                ]
        else:
            return []
    
    def dict_head(self, head):
        width = {
            self.first_field:300,
            'op':180,
            
        }
        head['width'] = width.get(head['name'])
        if head['name']==self.first_field:
            if not head.get('inn_tree_deep_editor'):
                head['inn_tree_deep_editor']= head['editor']
            head['editor'] = 'com-table-tree-first'
            #head['class']='chuizhi'
            #head['css']='''.chuizhi:first-child{margin-left:23px}'''
        return head    
    
    def dict_row(self, inst):
        return {
            'hasChildren':inst.hasChildren,               
        }    
    

def get_tree_option(model,label_field,value_field='pk',extra_fields=[],par=None,query=None):
    ls = []
    if not query:
        if par:
            ls.append({'value': getattr(par,value_field,None) ,'label':getattr(par,label_field),'parent':None}) 
            #query = model.objects.filter(parent=par)
            query = model.objects.filter(path__startswith=par.path)
            #for inst in model.objects.filter(parent=par):
                #dc = {'value': getattr(inst,value_field,None),'label':getattr(inst,label_field),'parent':inst.parent_id}
                #if extra_fields:
                    #for key in extra_fields:
                        #dc[key] = getattr(inst,key,None)
                #ls.append(dc)        
        else:
            query =  model.objects.all()
            #for inst in model.objects.all():
                #dc = {'value':getattr(inst,value_field,None),'label':getattr(inst,label_field),'parent':inst.parent_id}
                #if extra_fields:
                    #for key in extra_fields:
                        #dc[key] = getattr(inst,key,None)            
                #ls.append(dc)
    for inst in query:
        dc = {'value':getattr(inst,value_field,None),'label':getattr(inst,label_field),'parent':inst.parent_id}
        if extra_fields:
            for key in extra_fields:
                dc[key] = getattr(inst,key,None)            
        ls.append(dc)    
    
    children_dc = {}
    for row in ls:
        if row['parent']:
            if row['parent'] not in children_dc:
                children_dc[row['parent']] =[]
            children_dc[row['parent']] .append(row)
    for row in ls:
        if row['value'] in children_dc:
            row['children'] = children_dc[row['value']]
    
    outls =[]
    for row in ls:
        if not row['parent']:
            outls.append(row)
            
    
    #for row in list(ls):
        #row['children'] =[]
        #if row['parent']:
            #ls.remove(row)
        #for item in ls:
            #if item['parent'] == row['value']:
                #row['children'] .append(item)
        #if not row['children']:
            #del row['children']
    return outls