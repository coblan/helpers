from .table import ModelTable
from django.db.models import Count

class CascadTable(ModelTable):
    def getParents(self):
        if self.kw.get('id'):
            inst = self.model.objects.get(pk = self.kw.get('id') )
            par_inst = inst.parent
            ls =[]
            while par_inst:
                ls.append({'value':par_inst.pk,'label':str(par_inst)})
                par_inst = par_inst.parent
            return [{'value':'','label':'全部'}] + list( reversed(ls) )
        if self.kw.get('_par'):
            par_inst = self.model.objects.get(pk = self.kw.get('_par') )
            ls =[]
            while par_inst:
                ls.append({'value':par_inst.pk,'label':str(par_inst)})
                par_inst = par_inst.parent
            return [{'value':'','label':'全部'}] + list( reversed(ls) )
        else:
            return [{'value':'','label':'全部'}]    
    
    def inn_filter(self, query):
        if not self.kw.get('id'):
            # 如果直接查询ID，才使用par去查
            if self.kw.get('_par'):
                query = query.filter(parent_id = self.kw.get('_par'))
            else:
                query = query.filter(parent_id__isnull=True)
        model_name = self.model.__name__.lower()
        query = query.annotate(child_count=Count(model_name))
        return query 
    
    def getExtraHead(self):
        return [
            {'name':'child_count',
             'label':'子数量',
             'editor':'com-table-click',
             'click_express':'''
             scope.ps.vc.searchArgs._par=scope.row.pk;
             scope.ps.vc.search()'''}
        ]    
    
    def dict_row(self, inst):
        return {
            'child_count':inst.child_count
        }
    
    def get_operations(self):
        ops = super().get_operations()
        for op in ops:
            if op['name'] == 'add_new':
                op['preset_express']=''' 
                rt ={}
                var parents =  scope.ps.vc.parents 
                if(parents.length>1){
                    var last_parent = parents[parents.length-1]
                    rt['parent_id']=last_parent.value
                    rt['_parent_id_label'] = last_parent.label
                }
                
                '''
        director_name = self.get_director_name()
        ops+=[
            {'name':'cut','label':'剪切','editor':'com-btn',
             'click_express':'''
                var pks = ex.map( scope.ps.vc.selected,item=>{return item.pk} )
                if(pks.length>0){
                     ex.localSet('cascad_cut_children',pks)
                     cfg.toast('剪切成功')
                }else{
                    cfg.toast('至少选择一行数据')
                }
               
            '''},
            {'name':'past','label':'粘贴','editor':'com-btn',
             'click_express':'''
                var parents = scope.ps.vc.parents
                if(parents.length>1){
                    var last_parent = parents[parents.length-1].value
                }else{
                    var last_parent=''
                }
                var children = ex.localGet('cascad_cut_children',)
                if(children){
                    ex.director('%s').paste({parent:last_parent,children:children}).then(()=>{
                        scope.ps.vc.search()
                    })
                }
                 ex.localSet('cascad_cut_children','')
            '''%(director_name+'.edit')
             },
        ]
        return ops       