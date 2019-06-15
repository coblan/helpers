from helpers.director.shortcut import ModelTable

class ModelTableMobile(ModelTable):
    filterForm =''
    def get_operation(self):
        ops = super().get_operation()
        if self.filterForm:
            ops += [
                 {'name':'查询','action':'scope.head.filter_ctx.title="查询条件";scope.head.filter_ctx.row=scope.ps.search_args;live_root.open_live("live_fields",scope.head.filter_ctx)',
                     'filter_ctx':self.filterForm().get_head_context()}
            ]
        return ops

class FilterForm(object):
    def get_operations(self):
        ops =  [
            {'label':'查询','editor':'com-op-submit','action':'''
            var vc = ex.vueParStore(scope.ps.vc,function(vc){return vc.basename && vc.basename.startsWith("live-")}).vc; 
            var table = vc.$root.lastsibe(vc) ;
            ex.vueAssign(table.childStore.search_args,scope.ps.vc.row)
            table.childStore.search();
            window.history.back();
                       '''}
        ]
        return ops