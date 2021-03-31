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
            // 检查 rows的选中情况是否满足 head所标示
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
        },
        async selected_set_and_save(kws){
            /*
             这个是主力函数
             // 路线：弹出->编辑->update前端（缓存的）row->保存->后台->成功->update前端row->关闭窗口
             * */
            // head: row_match:many_row ,
            var self=this
            if(!this.check_selected(kws)){
                return
            }
            //如果有确认信息，弹框确认
            if(kws.confirm_msg){
                await cfg.confirm(kws.confirm_msg)
            }
            var first_sel_row = self.selected[0]
            var one_row={}
            let preset_express = kws.preset_express  //|| kws.pre_set
             if(preset_express ){
                var dc = ex.eval(preset_express,{ps:this.childStore,vc:this})
                ex.assign(one_row,dc)
            }
            // 有弹出编辑窗口的需求
            if(kws.fields_ctx){
                // 确保 前面 preset_express设置过的字段，这里不会被替换
                ex.each(kws.fields_ctx.heads,(head)=>{
                    if(!head.name.startsWith('_') && one_row[head.name]==undefined){
                        one_row[head.name]=self.selected[0][head.name]
                    }
                })
                // 将当前的ps 传递到弹出框中
                kws.fields_ctx.pop_vc = self
                var win_index = pop_edit_local(one_row,kws.fields_ctx,function(e){
                    if(e == '__end_by_user'){
                        return
                    }
                    var dc = {new_row:e.row,field_vc:e.vc,pop_fields_win_index:win_index}
                    after_proc(dc)
                })
            }else{
                after_proc({new_row:one_row})
            }

            function after_proc({new_row,field_vc,pop_fields_win_index}){
                /*
                 编辑后，提交

                 @new_row : 编辑后的 cache_row ,
                 * */

                var cache_rows = ex.copy(self.selected)
                ex.each(cache_rows ,function(row){
                    ex.assign(row,new_row)
                    if(kws.fields_ctx && kws.fields_ctx.director_name){
                        row._cache_director_name = row._director_name // [1] 有可能是用的特殊的 direcotor
                        row._director_name=kws.fields_ctx.director_name
                    }
                })
                cfg.show_load()
                ex.director_call('d.save_rows',{rows:cache_rows}).then((resp)=>{
                    cfg.hide_load()
                    if(resp._outdate){
                        layer.confirm(resp._outdate, {
                            icon:3,
                            title:'提示',
                            btn: ['刷新数据', '仍然保存', '取消'] //可以无限个按钮
                            ,btn3: function(index, layero){
                                layer.close(index)
                            }
                        }, function(index, layero){
                            layer.close(index)
                            var pk_list = ex.map(self.selected,(row)=>{return row.pk})
                            self.search().then(()=>{
                                /* 还原 selected
                                 并且更新弹出窗口的cache_row(也就是new_row)的数据.
                                 关于new_row,是在上一层函数中生成，并且排除了_开始的字段。在有弹出窗框时，new_row是selected[0],
                                 没有弹出框时,new_row可能没有字段，所以更新new_row时，需要判断 new_row[k] != undefined以免多增加了字段。
                                 */
                                self.selected = ex.filter(self.rows,(row)=>{return ex.isin(row.pk,pk_list)})
                                if(self.selected){
                                    for(var k in self.selected[0]){
                                        if(! k. startsWith('_')&& new_row[k] != undefined ){
                                            new_row[k]= self.selected[0][k]
                                        }
                                    }
                                }
                            })
                        }, function(index){
                            layer.close(index)
                            //ex.each(self.selected,row=>{
                            //    row.meta_overlap_fields='__all__'
                            //})
                            new_row.meta_overlap_fields = '__all__'
                            after_proc({new_row,field_vc,pop_fields_win_index})
                            //self.selected_set_and_save(kws,true)
                        });
                        return
                    }else  if( !resp.errors){
                        cfg.toast('操作成功！',{time:1000})
                        if(kws.after_save){
                            if(ex.eval(kws.after_save,{rows:resp,ps:self}) == 'stop'){
                                return
                            }
                        }
                        ex.each(resp,function(new_row){
                            // [1]  这里还原回去
                            if(new_row._cache_director_name){
                                new_row._director_name = new_row._cache_director_name
                            }
                            self.update_or_insert(new_row)
                        })

                        self.clearSelection()
                        if(pop_fields_win_index){
                            layer.close(pop_fields_win_index)
                        }

                    }else{
                        if(kws.save_error_express){
                            // 有弹出fields框时，设置 after_error ，显示错误
                            ex.eval(kws.save_error_express,{vc:field_vc,errors:resp.errors})
                        }else{
                            if (field_vc){
                                //field_vc.setErrors(resp.errors)
                                field_vc.showErrors(resp.errors)
                            }else{
                                cfg.showError(JSON.stringify( resp.errors))
                            }
                        }

                    }

                })
            }
        },
        clearSelection(){
            //this.selected.splice(0,this.selected.length)
            this.selected = []
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