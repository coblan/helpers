var table_store={
    data:function(){
         return {
             parents:[],
             heads:[],
             rows:[],
             row_filters:{},
             row_sort:{},
             row_pages:{},
             director_name:'',
             footer:[],
             selected:[],
             search_args:{}, //ex.parseSearch(),
             ops:[],
             crt_row:{},
             selectable:true,
             changed_rows:[],
             event_slots:[],
             option:{},
         }
    },
    mixins:[mix_ele_table_adapter],
    created:function(){
        var self=this
        ex.each(this.event_slots,function(router){
            self.$on(router.event,function(e){
                ex.eval(router.express,{event:e,ts:self})
            })
        })
        if(this.head){
            if(this.head.init_express){
                ex.eval(this.head.init_express,{par_row:this.par_row,ps:this,vc:this.vc})
            }
        }

    },
    computed:{
        changed:function(){
            return this.changed_rows.length != 0
        },
        has_select:function(){
            return this.selected.length !=0
        },
    },
    methods:{
        row_has_field(name){
            if(this.rows.length ==0){
                return false
            }else{
                return this.rows[0][name] != undefined
            }
        },
        express:function(kws){
            var self=this
            var row_match_fun = kws.row_match
            if(row_match_fun && ! row_match[row_match_fun](self,kws)){
                return
            }
            if(kws.confirm_msg){
                layer.confirm(kws.confirm_msg, {icon: 3, title:'提示'}, function(index){
                    layer.close(index);
                    ex.eval(kws.express,self)
                });
            }else {
                var real_kws = ex.copy(kws)
                if(kws.update_kws){
                    ex.assign(real_kws,ex.eval(real_kws,{ts:self,kws:kws}))
                }
                ex.eval(real_kws.express,{ts:self,kws:real_kws})
            }

        },
        search:function(){
            this.search_args._page=1
            this.getRows()
        },
        getRows:function(){
            /*
             以后都用这个函数，不用什么get_data 或者 data_getter 了
             * */
            var self=this

            cfg.show_load()
            //self.rows=[]

            var post_data=[{fun:'get_rows',director_name:self.director_name,search_args:self.search_args}]
            ex.post('/d/ajax',JSON.stringify(post_data),function(resp){
                self.rows = resp.get_rows.rows
                ex.vueAssign( self.row_pages,resp.get_rows.row_pages)
                //self.row_pages = resp.get_rows.row_pages
                //self.search_args=resp.get_rows.search_args
                ex.vueAssign(self.search_args,resp.get_rows.search_args)
                self.footer=resp.get_rows.footer
                self.parents=resp.get_rows.parents
                self.table_layout=resp.get_rows.table_layout
                cfg.hide_load()
            })
        },
        add_new:function(kws){
            var head =kws

            var self = this
            var fields_ctx=kws.fields_ctx
            var dc = {fun:'get_row',director_name:fields_ctx.director_name}

            if(kws.pre_set){
                var pre_set = ex.eval(kws.pre_set,{vc:self.vc,ps:self,search_args:self.search_args})
                ex.assign(dc,pre_set)
            }else if(kws.init_fields){ // 老的的调用，准备移除
                ex.assign(dc,kws.init_fields)
            }
            var post_data=[dc]
            cfg.show_load()
            ex.post('/d/ajax',JSON.stringify(post_data),function(resp){
                cfg.hide_load()
                var crt_row = resp.get_row
                if(self.search_args._par){
                    crt_row.meta_par=self.search_args._par
                }
                if(head.preset){
                    ex.vueAssign(crt_row,ex.eval(head.preset,{ts:self}))
                }
                self.crt_row= crt_row
                if(kws.tab_name){
                    // 需要继承table_page_store
                    //self.switch_to_tab(kws)
                    var bb = ex.copy(kws)
                    bb.par_row=crt_row
                    self.switch_to_tab(bb)
                    //self.$emit('operation',{fun:'switch_to_tab',tab_name:kws.tab_name,row:crt_row})
                    //self.switch_to_tab({tab_name:kws.tab_name,row:crt_row})

                }else{
                    var win=pop_fields_layer(crt_row,fields_ctx,function(new_row){
                        self.update_or_insert(new_row, crt_row)
                        layer.close(win)
                        if(kws.after_save){
                            ex.eval(kws.after_save,{ts:self})
                        }
                    })
                }
            })
        },
        pop_edit:function({row,fields_ctx,after_save}){
            var self=this
            var win_index =  pop_fields_layer(row,fields_ctx,function(new_row) {
                if(after_save){
                    ex.eval(after_save,{new_row:new_row,ps:self})
                }else{
                    self.update_or_insert(new_row)
                }
                //var fun = after_save[self.head.after_save.fun]
                //fun(self, new_row, pop_row)

                layer.close(win_index)
            })
            //var fun= get_row[this.head.get_row.fun]
            //if(this.head.get_row.kws){
            //    //  这个是兼顾老的调用，新的调用，参数直接写在get_row里面，与fun平级
            //    var kws= this.head.get_row.kws
            //}else{
            //    var kws= this.head.get_row
            //}
            //kws.director_name = this.head.fields_ctx.director_name

            //fun(function(pop_row){
            //    //pop_fields_layer(pop_row,self.head.fields_heads,ops,self.head.extra_mixins,function(kws){
            //    var win_index =  pop_fields_layer(pop_row,self.head.fields_ctx,function(new_row){
            //
            //        var fun = after_save[self.head.after_save.fun]
            //        fun(self,new_row,pop_row)
            //
            //        layer.close(win_index)
            //
            //    })
            //},this.rowData,kws)
        },

        clearSelection:function(){
            this.selected =[]
            // 在mix_ele_table_adaptor 中会触发 element table 自动清除选择。
        },
        get_childs:function(par){
            this.search_args._par=par
            this.search()
        },
        update_or_insert:function(new_row,old_row){
            // 如果是更新，不用输入old_row，old_row只是用来判断是否是创建的行为
            // 不用 old_row 了， 只需要判断 pk 是否在rows里面即可。
            var table_row = ex.findone(this.rows,{pk:new_row.pk})
            if(table_row){
                ex.vueAssign(table_row,new_row)
            }else{
                this.rows=[new_row].concat(this.rows)
                this.row_pages.total+=1
            }


            //if(old_row && ! old_row.pk) {
            //
            //    //var rows = this.rows.splice(0, 0, new_row)
            //    this.rows=[new_row].concat(this.rows)
            //    this.row_pages.total+=1
            //}else{
            //    var table_row = ex.findone(this.rows,{pk:new_row.pk})
            //    if(table_row){
            //        ex.vueAssign(table_row,new_row)
            //    }
            //}
            this.$emit('row.update_or_insert',[new_row])
        },
        update_rows:function(rows){
            var self=this
            ex.each(rows,function(row){
                var table_row = ex.findone(self.rows,{pk:row.pk})
                ex.vueAssign(table_row,row)
            })
            self.$emit('row.update_or_insert',[rows])
        },
        check_selected(head){
            var row_match_fun = head.row_match || 'many_row'
            return row_match[row_match_fun](this, head)
        },
        selected_set_and_save:function(kws,resend){
            /*
             这个是主力函数
             // 路线：弹出->编辑->update前端（缓存的）row->保存->后台->成功->update前端row->关闭窗口
             * */
            // head: row_match:many_row ,
            var self=this
            var row_match_fun = kws.row_match || 'many_row'
            if(! row_match[row_match_fun](self,kws)){
                return
            }

                /*
                弹框确认
                * */
                new Promise(function(resolve,reject){
                    if(kws.confirm_msg && !resend){
                        layer.confirm(kws.confirm_msg, {icon: 3, title:'提示'}, function(index){
                            layer.close(index);
                           resolve()
                        });
                    }else {
                        resolve()
                    }
                }).then(function(){
                    //  弹出编辑框/ 或者不弹出
                        var one_row={}
                        if(kws.field){ // 兼容老的，新的采用eval形式，
                            one_row[kws.field]=kws.value
                            one_row.meta_overlap_fields =kws.field
                        }else if(kws.pre_set){
                            var dc = ex.eval(kws.pre_set)
                            ex.assign(one_row,dc)
                            one_row.meta_overlap_fields = Object.keys(dc).join(',')
                        }

                        if(kws.fields_ctx){
                            ex.map(kws.fields_ctx.heads,function(head){
                                if(!head.name.startsWith('_') && one_row[head.name]==undefined){
                                    one_row[head.name]=self.selected[0][head.name]
                                }
                            })
                            var win_index = pop_edit_local(one_row,kws.fields_ctx,function(new_row,store){
                                var dc = {new_row:new_row,field_store:store,pop_fields_win_index:win_index}
                                after_proc(dc)
                            })
                        }else{
                            after_proc({new_row:one_row})
                        }
                }
            )

            function after_proc({new_row,field_store,pop_fields_win_index}){
                // 编辑后，提交
                var cache_rows = ex.copy(self.selected)
                ex.each(cache_rows ,function(row){
                    ex.assign(row,new_row)
                    if(kws.fields_ctx && kws.fields_ctx.director_name){
                        row._cache_director_name = row._director_name // [1] 有可能是用的特殊的 direcotor
                        row._director_name=kws.fields_ctx.director_name
                    }
                    //row[kws.field]=kws.value
                })
                var post_data=[{fun:'save_rows',rows:cache_rows}]
                cfg.show_load()
                ex.post('/d/ajax',JSON.stringify(post_data),function(resp){
                    if(resp.save_rows._outdate){
                        layer.confirm(resp.save_rows._outdate, {
                            icon:3,
                            title:'提示',
                            btn: ['刷新数据', '仍然保存', '取消'] //可以无限个按钮
                            ,btn3: function(index, layero){
                                layer.close(index)
                            }
                        }, function(index, layero){
                            layer.close(index)
                            self.search()
                        }, function(index){
                            layer.close(index)
                            ex.each(self.selected,row=>{
                                row.meta_hash_fields=''
                            })
                            self.selected_set_and_save(kws,true)
                        });
                        return
                    }
                    if( !resp.save_rows.errors){
                        if(kws.after_save){
                            if(ex.eval(kws.after_save,{rows:resp.save_rows,ps:self}) == 'stop'){
                                return
                            }
                        }
                        ex.each(resp.save_rows,function(new_row){
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
                        cfg.hide_load(2000)
                    }else{
                        cfg.hide_load()
                        if(kws.after_error){
                            ex.eval(kws.after_error,{fs:field_store,errors:resp.save_rows.errors})
                        }else{
                            cfg.showError(JSON.stringify( resp.save_rows.errors))
                        }

                    }

                })
            }





            //row[kws.field]=kws.value


            //if(kws.confirm_msg){
            //    layer.confirm(kws.confirm_msg, {icon: 3, title:'提示'}, function(index){
            //        layer.close(index);
            //        judge_pop_fun()
            //    });
            //}else {
            //    judge_pop_fun()
            //}
        },
        export_excel:function(){
            var self=this
            var search_args = ex.copy(self.search_args)
            search_args._perpage=5000
            var post_data=[{fun:'get_excel',director_name:self.director_name,search_args:search_args}]
            cfg.show_load()
            ex.post('/d/ajax',JSON.stringify(post_data),function(resp){
                cfg.hide_load()
                var url = resp.get_excel.file_url
                ex.download(url)
            })
        },
        director_call:function(kws){
            var self =this
            var row_match_fun = kws.row_match
            if(row_match_fun && ! row_match[row_match_fun](self,kws)){
                return
            }


            function do_director_call(new_row,callback){
                cfg.show_load()
                ex.director_call(kws.director_name,{rows:self.selected,new_row:new_row},function(resp){
                    if(!resp.msg){
                        cfg.hide_load(2000)
                    }else{
                        cfg.hide_load()
                    }
                    if(kws.after_save){
                        ex.eval(kws.after_save,{resp:resp,ts:self})
                    }else{
                        // 兼容老的调用
                        // 返回rows ，默认更新
                        if(resp.rows){
                            self.update_rows(resp.rows)
                        }
                        if(resp.row){
                            self.update_or_insert(resp.row)
                        }
                    }

                    self.clearSelection()
                    if(callback){
                        callback(resp)
                    }
                })
            }

            function judge_pop_fun(){
                var one_row={}
                ex.assign(one_row,ex.eval(kws.pre_set,{head:kws,ps:self.parStore}))
                if(kws.fields_ctx){
                    ex.map(kws.fields_ctx.heads,function(head){
                        if(!head.name.startsWith('_') && one_row[head.name]==undefined){
                            one_row[head.name]=self.selected[0][head.name]
                        }
                    })
                    var win_index = pop_edit_local(one_row,kws.fields_ctx,function(new_row,store){
                        do_director_call(new_row,function(resp){
                            layer.close(win_index)
                        })
                    })
                }else{
                    do_director_call(one_row)
                }
            }

            if(kws.confirm_msg){
                layer.confirm(kws.confirm_msg, {icon: 3, title:'提示'}, function(index){
                    layer.close(index)
                    judge_pop_fun()
                })
            }else{
                judge_pop_fun()
            }
        },
        arraySpanMethod:function({ row, column, rowIndex, columnIndex }){
            // 计算布局
            if(this.table_layout){
                return this.table_layout[`${rowIndex},${columnIndex}`] || [1,1]
            }else{
                return [1,1]
            }
        },
        delete_selected:function(){
            var self=this
            layer.confirm('真的删除吗?', {icon: 3, title:'确认'}, function(index) {
                layer.close(index);
                //var ss = layer.load(2);
                cfg.show_load()
                var post_data = [{fun: 'del_rows', rows: self.selected}]
                ex.post('/d/ajax', JSON.stringify(post_data), function (resp) {
                    cfg.hide_load()
                    self.search()
                })
            })
        },
        pop_panel:function(kws){
            var self=this
            var row_match_fun = kws.row_match || 'many_row'
            if(! row_match[row_match_fun](self,kws)){
                return
            }
            if(kws.panel){
                var panel = kws.panel
            }else{
                var panel = ex.eval(kws.panel_express,{ts:self,kws:kws})
            }
            var ctx = ex.copy(kws)
            if(kws.ctx_express){
                var cus_ctx = ex.eval(kws.ctx_express,{ts:self,kws:kws})
                ex.assign(ctx, cus_ctx )
            }
            var winclose = cfg.pop_middle(panel,ctx,function(resp){
                if(ctx.after_express){
                    ex.eval(ctx.after_express,{ts:self,resp:resp})
                }else{
                    self.update_or_insert(resp)
                }
                self.clearSelection()
                winclose()
            })
        }
    }

}

var row_match={
    one_row:function(self,head){
        if(self.selected.length ==0){
            cfg.showMsg('请选择一条数据！')
            return false
        }else if(self.selected.length >1){
            cfg.showMsg('只能选择一条数据！')
            return false
        }else if(head.match_express){
                var matched= ex.eval(head.match_express,{row:self.selected[0]})
                if(!matched){
                    cfg.showError(head.match_msg)
                    return false
                }
        }
        return true
    },
    many_row:function(self,head){
        if(self.selected.length ==0 ){
            cfg.showMsg('请至少选择一条数据！')
            return false
        }else{
            if(head.match_express){
                for (var i=0;i<self.selected.length;i++){
                    var row = self.selected[i]
                    if( !ex.eval(head.match_express,{row:row}) ){
                        cfg.showError(head.match_msg)
                        return false
                    }
                }
            }
            return true
        }
    },
    one_row_match:function(self,head){
        if(self.selected.length !=1 ){
            cfg.showMsg('请选择一行数据！')
            return false
        }else{
            var field=head.match_field
            var values = head.match_values
            var msg = head.match_msg

            var row = self.selected[0]

            if( ! ex.isin(row[field],values ) ) {
                cfg.showMsg(msg)
                return false
            }else{
                return true
            }
        }
    },
    // 这个函数被 many_row 替代了。 只需要加上 match_express 就可以替换这个函数
    many_row_match:function(self,head){
        // head : @match_field , @match_values ,@match_msg
        if(self.selected.length ==0 ){
            cfg.showMsg('请至少选择一行数据！')
            return false
        }else{
            if(head.match_field){ // 老的用法，准备剔除  ,现在全部改用 match_express
                var field=head.match_field
                var values = head.match_values
                var msg = head.match_msg

                for (var i=0;i<self.selected.length;i++){
                    var row = self.selected[i]
                    if( ! ex.isin(row[field],values ) ){
                        cfg.showMsg(msg)
                        return false
                    }
                }
                return true
            }else{
                for (var i=0;i<self.selected.length;i++){
                    var row = self.selected[i]
                    if( !ex.eval(head.match_express)){
                        cfg.showMsg(head.match_msg)
                        return false
                    }
                }
                return true
            }

        }
    },
}

window.table_store= table_store