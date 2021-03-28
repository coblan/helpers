export default {
    methods:{
         async addNew(kws){
            // @kws : 传入的 button的 head
            var self = this
            var fields_ctx=kws.fields_ctx
            var dc = {director_name:fields_ctx.director_name}
            if(kws.preset_express){
                var pre_set = ex.eval(kws.preset_express,{vc:self.vc,ps:self,search_args:self.searchArgs})
                ex.assign(dc,pre_set)
            }
            cfg.show_load()
            let resp = await ex.director_call('d.get_row',dc)
            cfg.hide_load()
             fields_ctx.row= resp
             let row = await cfg.pop_vue_com('com-form-one',fields_ctx)
             if(row){
                 self.update_or_insert(row)
                 if(kws.after_save_express){
                     ex.eval(kws.after_save_express,{vc:self.vc,ps:self.childStore,search_args:self.searchArgs,row:row})
                 }
             }
        },
        update_or_insert(new_row){
            var table_row = ex.findone(this.tableRows,{pk:new_row.pk})
            if(table_row){
                ex.vueAssign(table_row,new_row)
            }else{
                this.tableRows.splice(0,0,new_row) //  [new_row].concat(this.tableRows)
                this.rowPages.total+=1
            }
            this.$emit('row.update_or_insert',[new_row])
        },
        check_selected(head){
            //@head 是button的参数
            return new Promise((resolve,reject)=>{
                var row_match_fun = head.row_match || 'many_row'
                if(row_match[row_match_fun](this, head)) {
                    resolve()
                }else{
                    reject()
                }
            })
        },
        async delete_selected(){
            //return new Promise((resolve,reject)=>{
            await cfg.confirm("确认删除选中项?")
            cfg.show_load()
            await ex.director_call('d.delete_rows',{rows:this.selected})
            cfg.hide_load()
            this.search()
            //resolve()
                //layer.confirm('确认删除选中项?', {icon: 3, title:'确认'}, function(index) {
                //    layer.close(index);
                //    //var ss = layer.load(2);
                //    cfg.show_load()
                //    var post_data = [{fun: 'del_rows', rows: self.selected}]
                //    ex.post('/d/ajax', JSON.stringify(post_data), function (resp) {
                //        cfg.hide_load()
                //        self.search()
                //        resolve()
                //    })
                //})
            //})

        },
    }

}


var row_match= {
    one_row: function (self, head) {
        if (self.selected.length == 0) {
            cfg.showMsg('请选择一条数据！')
            return false
        } else if (self.selected.length > 1) {
            cfg.showMsg('只能选择一条数据！')
            return false
        } else if (head.match_express) {
            var matched = ex.eval(head.match_express, {row: self.selected[0]})
            if (!matched) {
                cfg.showError(head.match_msg)
                return false
            }
        }
        return true
    },
    many_row: function (self, head) {
        if (self.selected.length == 0) {
            cfg.showMsg('请至少选择一条数据！')
            return false
        } else {
            if (head.match_express) {
                for (var i = 0; i < self.selected.length; i++) {
                    var row = self.selected[i]
                    if (!ex.eval(head.match_express, {row: row})) {
                        cfg.showError(head.match_msg)
                        return false
                    }
                }
            }
            return true
        }
    },
}