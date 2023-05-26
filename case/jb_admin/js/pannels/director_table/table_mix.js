export default {
    methods:{
         async addNew(kws){
            // @kws : 传入的 button的 head
            var self = this
            var fields_ctx=kws.fields_ctx
            var dc = {director_name:fields_ctx.director_name}
            if(kws.preset_express){
                var pre_set = ex.eval(kws.preset_express,{vc:self,ps:self.childStore,search_args:self.searchArgs})
                ex.assign(dc,pre_set)
            }
            cfg.show_load()
            let resp = await ex.director_call('d.get_row',dc)
            cfg.hide_load()
             fields_ctx.row= resp
             let row = await cfg.pop_vue_com('com-form-one',fields_ctx,{maxmin: true})
             if(row){
                 self.update_or_insert(row)
                 if(kws.after_save_express){
                     ex.eval(kws.after_save_express,{vc:self,ps:self.childStore,search_args:self.searchArgs,row:row})
                 }
             }
            debugger
            return row
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
            var self =this;

            return new Promise((resolve,reject)=>{

                var row_match_fun = head.row_match || 'many_row'

                if(row_match[row_match_fun](this, head)) {
                    resolve()

                }else{
                     reject()
                }

                // if (head.match_express) {
                //     for (var i = 0; i < self.selected.length; i++) {
                //         var row = self.selected[i]
                //         if (!ex.eval(head.match_express, {row: row})) {
                //             // cfg.showError(head.match_msg)
                //             reject()
                //         }
                //     }
                // }


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
            debugger
            var self=this
            //if(!this.check_selected(kws)){
            //    return
            //}
            //如果有确认信息，弹框确认
            //if(kws.confirm_msg){
            //    await cfg.confirm(kws.confirm_msg)
            //}
            //var first_sel_row = self.selected[0]
            if(kws.preset_express){
                var one_row = ex.eval(kws.preset_express,{ps:this.childStore,vc:this})
            }else if(kws.preset){
                var one_row = ex.copy(kws.preset)
            }else{
                var one_row = {}
            }
            // 有弹出编辑窗口的需求
            if(kws.fields_ctx){
                // 确保 前面 preset_express设置过的字段，这里不会被替换
                //ex.each(kws.fields_ctx.heads,(head)=>{
                //    if(!head.name.startsWith('_') && one_row[head.name]==undefined){
                //        one_row[head.name]=self.selected[0][head.name]
                //    }
                //})

                //ex.vueAssign(one_row,self.selected[0])

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
                after_proc({new_row:one_row,director_full_field:kws.director_full_field})
            }

            function after_proc({new_row,field_vc,pop_fields_win_index,director_full_field=true}){
                /*
                 编辑后，提交

                 @new_row : 编辑后的 cache_row ,
                 * */
                if(director_full_field){
                    var cache_rows = ex.copy(self.selected)
                    ex.each(cache_rows ,function(row){
                        ex.assign(row,new_row)
                        // 2021/4/22去掉根据弹出框fields的ctx 切换director_name.因为如果有用ctx保存的需求，可以直接弹出fields框。
                        //if(kws.fields_ctx && kws.fields_ctx.director_name){
                        //    row._cache_director_name = row._director_name // [1] 有可能是用的特殊的 direcotor
                        //    row._director_name=kws.fields_ctx.director_name
                        //}
                    })
                }else{
                    var cache_rows = []
                    ex.each(self.selected,(row)=>{
                        var tmp_row = {
                            pk:row.pk,
                            _director_name:row._director_name,
                            meta_director_full_field:false,
                            ...new_row
                        }
                        cache_rows.push(tmp_row)
                    })
                }

                cfg.show_load()
                ex.director_call('d.save_rows',{rows:cache_rows}).then((resp)=>{
                    cfg.hide_load()
                    if(resp._outdate){
                        layer.confirm(resp._outdate, {
                            icon:3,
                            title:'提示',
                            btn:  ['刷新数据', '取消'] , //  ['刷新数据', '仍然保存', '取消'] //可以无限个按钮
                            btn3: function(index, layero){
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
                            //  [1]  这里还原回去 // 注释原因见上面的[1]
                            //if(new_row._cache_director_name){
                            //    new_row._director_name = new_row._cache_director_name
                            //}
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
        getChilds:function(par){
            this.searchArgs._par=par
            this.search()
        },
        search({loading=true,clear_row=true}={}){
            this.search_page(1,{loading,clear_row})
        },
        switchToTab:function(kws){
            // 从 table_page_store 移过来的。因为 live_table 可能有这个需求
            var self=this
            var tabs=named_ctx[kws.ctx_name]
            if(!tabs){
                throw `named_ctx. ${kws.ctx_name} 不存在，检查是否传入`
            }

            var canfind = ex.findone(tabs,{name:kws.tab_name})
            if(!kws.tab_name || !canfind ){
                kws.tab_name = tabs[0].name
            }

            if(window.root_live){
                // keeplive 页面
                root_live.open_live(live_el_tab,{tabs:tabs,
                    title:kws.par_row._label,crt_tab_name:kws.tab_name,par_row:kws.par_row,
                    type:kws.type,
                    top_editor: kws.top_editor,
                    top_ctx: kws.top_ctx,
                    last_ps:self})
            }else{
                root_store.$emit('switch-to-tab',{
                    widget:'com-widget-el-tab' ,
                    tabs:tabs,
                    crt_tab_name:kws.tab_name,
                    par_row:kws.par_row,
                    type:kws.type,
                    top_editor: kws.top_editor,
                    top_ctx: kws.top_ctx,
                })
                // 传统 页面
                //self.tab_stack.push( {
                //    widget:'com-widget-el-tab' ,
                //    tabs:tabs,
                //    crt_tab_name:kws.tab_name,
                //    par_row:kws.par_row,
                //
                //})
            }
            // 这里暂时打开，以后移除
            self.crt_row=kws.par_row
        },

        exportExcel(head){
            debugger
            var self=this
            var head = head || {}
            var search_args = ex.copy(self.searchArgs)
            search_args._perpage= head.count || 5000
            var post_data=[{fun:'get_excel',director_name:self.directorName,search_args:search_args}]
            cfg.show_load()
            ex.post('/d/ajax',JSON.stringify(post_data),function(resp){
                cfg.hide_load()
                var url = resp.get_excel.file_url
                ex.download(url)
            })
        },

        //  element table 专用方法
        sortChange(params){
            //{ column, prop, order }
            var self=this
//                this.$refs.e_table.clearSort()
//                ex.each(this.row_sort.sortable,function(name){
            if(params.prop){
                if(params.order=='ascending'){
                    self.searchArgs._sort=params.prop
                }else if(params.order=='descending'){
                    self.searchArgs._sort='-'+params.prop
                }
            }else{
                self.searchArgs._sort=''
            }
            this.search()
//                })

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