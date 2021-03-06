from helpers.director.shortcut import ModelTable,Fields,director,get_request_cache

class FilterForm(object):
    def get_operations(self):
        ops =  [
            {'label':'查询','editor':'com-op-submit','action':'''
            var vc = ex.vueParStore(scope.ps.vc,function(vc){return vc.basename && vc.basename.startsWith("live-")}).vc; 
            var table = vc.$root.lastsibe(vc) ;
            ex.vueAssign(table.childStore.search_args,scope.ps.vc.row)
            table.childStore.search();
            window.history.back();
                       '''},
            {'label':'清空条件','editor':'com-op-submit','type':'default',
             'action':'''
             var vc = ex.vueParStore(scope.ps.vc,function(vc){return vc.basename && vc.basename.startsWith("live-")}).vc; 
            var table = vc.$root.lastsibe(vc) ;
            table.childStore.search_args={}; table.childStore.search();window.history.back();'''}
        ]
        return ops
    def set_filter(self,table_filter):
        self.table_filter = table_filter
    
    def map_content(self,filter_heads):
        heads =[]
        for head in filter_heads:
            if head['editor'] in ['com-select-filter','com-filter-select']:
                head['editor'] ='com-field-select'
                heads.append(head)
            if head['editor'] in ['com-date-datetimefield-range-filter',]:
                heads.append({
                    'name':'_start_%s'%head['name'],'label':'开始'+head['label'],'editor':'com-field-date'
                })
                heads.append({
                     'name':'_end_%s'%head['name'],'label':'结束'+head['label'],'editor':'com-field-date'
                })
            if head['editor'] in ['com-filter-datetime-range']:
                heads.append({
                    'name':'_start_%s'%head['name'],'label':'开始'+head['label'],'editor':'com-field-datetime'
                })
                heads.append({
                     'name':'_end_%s'%head['name'],'label':'结束'+head['label'],'editor':'com-field-datetime'
                })
            if head['editor'] in ['com-filter-text']:
                head['editor'] = 'com-field-linetext'
                heads.append(head)
        return heads
    
    def get_heads(self):
        filter_ctx = self.table_filter.get_context()
        heads = self.map_content(filter_ctx)
        return heads

class ModelTableMobile(ModelTable):
    filterForm =''
    
    def get_head_context(self):
        ctx = super().get_head_context()
        named_ctx = get_request_cache()['named_ctx']
        director_name = self.get_director_name()
        editor_director = director_name+'.edit'
        
        fieldCls = director.get(editor_director)     
        if not  fieldCls:
            return ctx
        if not editor_director in director_name:
            fom = fieldCls()
            form_ctx = fom.get_head_context()
            if 'after_save' not in form_ctx:
                form_ctx['after_save']='cfg.toast("保存成功"); scope.vc.ctx.genStore.update_or_insert(scope.row);'
            named_ctx[editor_director] = form_ctx

        ctx.update( {
            'table_editor': 'com-list-row-cell',#'com-ctn-table-van-cell',
            'block_click':''' var dynctx =named_ctx["%(edit_form)s"];
            dynctx.genStore=scope.ps;dynctx.row=scope.row;dynctx.title=dynctx.row._label;live_root.open_live("live_fields",dynctx) 
            ''' %{'edit_form':editor_director},
        }) 
        return ctx

    def get_operation(self):
        ops=[]
        director_name = self.get_director_name()
        fieldCls = director.get(director_name+'.edit')     
        if  fieldCls:
            #fieldobj=fieldCls(crt_user=self.crt_user)
            # 这里用name是逼不得已，因为vant只接受name作为其label
            ops = [
                {'name':'add_new',
                 'label':'新增',
                 'icon_editor':'com-nav-vant-icon',
                 'icon_ctx':{'name':'plus'},
                 'level':'rigth-top',
                 'action':'scope.ps.newRow().then((row)=>{var fields_ctx = named_ctx["%(editor_director_name)s"]; fields_ctx.row=row;fields_ctx.genStore=scope.ps; live_root.open_live("live_fields",fields_ctx)   })'%{'editor_director_name':director_name+'.edit'}}
            ]
        
        filter_obj = self.filterForm()
        filter_obj.set_filter(self.row_filter)
        if self.row_filter.names and self.filterForm:
            ops += [
                 {'name':'search',
                  'label':'查询',
                  'icon_editor':'com-nav-vant-icon',
                 'icon_ctx':{'name':'search'},
                 'level':'rigth-top',
                  'action':'scope.head.filter_ctx.title="查询条件";scope.head.filter_ctx.row=scope.ps.search_args;live_root.open_fade("live_fields",scope.head.filter_ctx)',
                     'filter_ctx':filter_obj.get_head_context()}
            ]
        return ops
    class filterForm(FilterForm,Fields):
        pass
    

#class ModelTablePickerMobile(ModelTableMobile):
    #def get_context(self):
        #ctx = super().get_context()
        #ctx['block_click'] ='scope.ps.par_row.staff= scope.row.user; scope.ps.par_row._staff_label=scope.row.name ; history.back()'
        #return ctx
