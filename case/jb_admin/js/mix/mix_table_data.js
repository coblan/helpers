var mix_table_data={
    data:function(){
        return {
            op_funs:{},
            changed_rows:[],

            table_layout:{},
        }
    },
    mounted:function(){
        var self=this
        ex.assign(this.op_funs,{
            save_changed_rows:function(){
                self.save_rows(self.changed_rows)
                self.changed_rows=[]
            },
            add_new:function(kws){
                /*
                * model_name,
                * */
                self.add_new(kws)
            },
            delete:function(){
                self.del_selected()
            },
            get_data:function(){
                self.getRows()
            },
            selected_set_value:function(kws){
                /* kws ={ field,value }
                * */
                ex.each(self.selected,function(row){
                    row[kws.field]=kws.value
                    if(row._hash != ex.hashDict(row)){
                        if(!ex.isin(row,self.changed_rows)){
                            self.changed_rows.push(row)
                        }
                    }
                })
            },
            selected_set_and_save:function(kws){
                /*
                这个是主力函数
                 // 路线：弹出->编辑->update前端（缓存的）row->保存->后台->成功->update前端row->关闭窗口
                * */
                // head: row_match:many_row ,
              var row_match_fun = kws.row_match || 'many_row'
               if(! row_match[row_match_fun](self,kws)){
                   return
               }

                function  bb(all_set_dict,after_save_callback){
                    var cache_rows = ex.copy(self.selected)
                    ex.each(cache_rows ,function(row){
                        ex.assign(row,all_set_dict)
                        if(kws.fields_ctx && kws.fields_ctx.director_name){
                            row._cache_director_name = row._director_name // [1] 有可能是用的特殊的 direcotor
                            row._director_name=kws.fields_ctx.director_name
                        }
                        row[kws.field]=kws.value
                    })
                    var post_data=[{fun:'save_rows',rows:cache_rows}]
                    cfg.show_load()
                    ex.post('/d/ajax',JSON.stringify(post_data),function(resp){
                        if( !resp.save_rows.errors){
                            ex.each(resp.save_rows,function(new_row){
                                delete new_row._director_name  // [1]  这里还原回去
                                self.update_or_insert(new_row)
                            })
                            cfg.hide_load(2000)
                        }else{
                            cfg.hide_load()
                            // 留到下面的field弹出框，按照nicevalidator的方式去显示错误
                            //cfg.showError(resp.save_rows.msg)
                        }


                        //self.op_funs.update_or_insert_rows({rows:resp.save_rows} )

                        if(after_save_callback){
                            after_save_callback(resp)
                        }

                    })
                }

                function judge_pop_fun(){
                    if(kws.fields_ctx){
                        var one_row = ex.copy(self.selected[0])
                        var win_index = pop_edit_local(one_row,kws.fields_ctx,function(new_row,store_id){
                            bb(new_row,function(resp){
                                if(resp.save_rows.errors){
                                    self.$store.commit(store_id+'/showErrors',resp.save_rows.errors)
                                }else{
                                    layer.close(win_index)
                                }

                            })
                        })
                    }else{
                        bb({})
                    }
                }


                if(kws.confirm_msg){
                    layer.confirm(kws.confirm_msg, {icon: 3, title:'提示'}, function(index){
                        layer.close(index);
                        judge_pop_fun()
                    });
                }else {
                   judge_pop_fun()
                }
            },
            selected_pop_set_and_save:function(kws){
                // 被  selected_set_and_save 取代了。
                // 路线：弹出->编辑->保存->后台(成功)->update前端row->关闭窗口
                var row_match_fun = kws.row_match || 'one_row'
                if(! row_match[row_match_fun](self,kws)){
                    return
                }

                var crt_row =  self.selected[0]
                var cache_director_name = crt_row._director_name
                crt_row._director_name = kws.fields_ctx.director_name
                var win_index = pop_fields_layer(crt_row,kws.fields_ctx,function(new_row){
                        ex.assign(crt_row,new_row)
                        crt_row._director_name=cache_director_name
                        layer.close(win_index)
                })
            },
            ajax_row:function(kws){
                // kws 是head : {'fun': 'ajax_row', 'app': 'maindb', 'ajax_fun': 'modify_money_pswd', 'editor': 'com-op-btn', 'label': '重置资金密码', },
                if(self.selected.length==0){
                    cfg.showMsg('请选择一行数据')
                    return
                }
                var row = self.selected[0]
                var post_data=[{fun:kws.ajax_fun,row:row  }]

                cfg.show_load()
                ex.post('/d/ajax/'+kws.app,JSON.stringify(post_data),function(resp){
                    cfg.hide_load(2000)
                })
            },
        create_child_row:function(kws){
            /*
             * */
            if(kws.fields_ctx ){
                var fields_ctx=kws.fields_ctx
                var dc = {fun:'get_row',director_name:fields_ctx.director_name}
                if(kws.init_fields){
                    ex.assign(dc,kws.init_fields)
                }
                var post_data=[dc]
                cfg.show_load()
                ex.post('/d/ajax',JSON.stringify(post_data),function(resp){
                    cfg.hide_load()
                    var crt_row = resp.get_row
                    self.crt_row= crt_row
                    crt_row.carry_parents = self.parents

                    if(kws.tab_name){
                        self.$emit('operation',{fun:'switch_to_tab',tab_name:kws.tab_name,row:crt_row})
                    }else{
                        var win=pop_fields_layer(crt_row,fields_ctx,function(new_row){
                            layer.close(win)
                            if(kws.after_save=='refresh'){
                                self.search()
                            }else{
                                self.update_or_insert(new_row, crt_row)
                            }
                        })
                    }

                })



                //var row={
                //    _director_name:kws.fields_ctx._director_name
                //}
                //pop_edit_local(row,kws.fields_ctx,function(new_row){
                //    cfg.show_load()
                //    ex.director_call(kws.fields_ctx.director_name,{row:new_row,parents:self.parents},function(resp){
                //        cfg.hide_load(300)
                //        self.update_or_insert(resp.row)
                //    })
                //})
            }
        },

            director_call:function(kws){
                function bb(){
                    cfg.show_load()
                    ex.director_call(kws.director_name,{},function(resp){
                        if(!resp.msg){
                            cfg.hide_load(2000)
                        }else{
                            cfg.hide_load()
                        }
                        if(kws.after_call){
                            self.op_funs[kws.after_call](resp)
                            if(resp.msg){
                                cfg.showMsg(resp.msg)
                            }
                        }
                    })
                }

                if(kws.confirm_msg){
                    layer.confirm(kws.confirm_msg, {icon: 3, title:'提示'}, function(index){
                        layer.close(index)
                        bb()
                    })
                }else{
                    bb()
                }
            },
            director_rows:function(kws){
                // kws: {after_call:'update_or_insert_rows'}
                var row_match_fun = kws.row_match || 'one_row'
                if(! row_match[row_match_fun](self,kws)){
                    return
                }

                function bb(){
                    cfg.show_load()
                    ex.director_call(kws.director_name,{rows:self.selected,},function(resp){
                        if(!resp.msg){
                            cfg.hide_load(2000)
                        }else{
                            cfg.hide_load()
                        }
                        if(kws.after_call){
                            self.op_funs[kws.after_call](resp)
                            if(resp.msg){
                                cfg.showMsg(resp.msg)
                            }
                        }
                    })
                }

                if(kws.confirm_msg){
                    layer.confirm(kws.confirm_msg, {icon: 3, title:'提示'}, function(index){
                        layer.close(index)
                        bb()
                    })
                }else{
                    bb()
                }
            },
            emitEvent:function(e){
                self.$emit(e)
            },

            update_or_insert:function(kws){
                self.update_or_insert(kws.new_row,kws.old_row)
            },
            update_or_insert_rows:function(kws){
                var rows = kws.rows
                ex.each(rows,function(row){
                    self.update_or_insert(row)
                })
            },

            export_excel:function(){
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

            // 为了刷新界面，付出了清空的代价，这两个函数小心使用，
            row_up:function(kws){
                var row=kws.row
                var index =self.rows.indexOf(row)
                if(index >=1 ){
                    var ss = swap(self.rows,index-1,index)
                    //self.rows=[]
                    //Vue.nextTick(function(){
                    //    self.rows=ss
                    //})

                }
                //self.$refs.core_table.sort()
            },
            row_down:function(kws){
                var row=kws.row
                var index =self.rows.indexOf(row)
                if(index < self.rows.length-1 ){
                    //Vue.set(self,'rows',swap(self.rows,index+1,index))
                    //self.rows =
                    var ss = swap(self.rows,index+1,index)
                    //self.rows=[]
                    //Vue.nextTick(function(){
                    //    self.rows=ss
                    //})
                }
                //self.$refs.core_table.sort()
            }

        })
        //this.$refs.op_save_changed_rows[0].set_enable(false)
        //this.$refs.op_delete[0].set_enable(false)
    },
    computed:{
        changed:function(){
            return this.changed_rows.length != 0
        },
        has_select:function(){
            return this.selected.length !=0
        },
    },

    methods: {
        on_operation:function(kws){
            var fun_name = kws.fun || kws.name
            this.op_funs[fun_name](kws)
        },
        on_td_event:function(kws){
            var fun_name = kws.fun || kws.name
            this.op_funs[fun_name](kws)
            //this.op_funs[e.name](e)
        },
        search:function(){
            this.search_args._page=1
            this.getRows()
        },
        add_new:function(kws){
            var self = this
            var fields_ctx=kws.fields_ctx
            var dc = {fun:'get_row',director_name:fields_ctx.director_name}
            if(kws.init_fields){
                ex.assign(dc,kws.init_fields)
            }
            var post_data=[dc]
            cfg.show_load()
            ex.post('/d/ajax',JSON.stringify(post_data),function(resp){
                cfg.hide_load()
                var crt_row = resp.get_row
                //var pop_id= new Date().getTime()
                // e = {name:'after_save',new_row:event.new_row,old_row:event.old_row}
                //eventBus.$on('pop-win-'+pop_id,function(e){
                //    self.update_or_insert(e.new_row, e.old_row)
                //})
                //pop_fields_layer(new_row,kws.heads,kws.ops,pop_id)
                self.crt_row= crt_row
                if(kws.tab_name){
                    //self.switch_to_tab(kws)
                    self.$emit('operation',{fun:'switch_to_tab',tab_name:kws.tab_name,row:crt_row})
                    //self.switch_to_tab({tab_name:kws.tab_name,row:crt_row})

                }else{
                    var win=pop_fields_layer(crt_row,fields_ctx,function(new_row){
                        self.update_or_insert(new_row, crt_row)
                        layer.close(win)
                    })
                }

            })
        },
        editRow:function(kws){
            var row=kws.row
            var fields_ctx = kws.fields_ctx

        },
        update_or_insert:function(new_row,old_row){
            // 如果是更新，不用输入old_row，old_row只是用来判断是否是创建的行为
            if(old_row && ! old_row.pk) {

                //var rows = this.rows.splice(0, 0, new_row)

                this.rows=[new_row].concat(this.rows)
                this.row_pages.total+=1

            }else{
                var table_row = ex.findone(this.rows,{pk:new_row.pk})
                //ex.assign(table_row,new_row)
                for(var key in new_row){
                    Vue.set(table_row,key,new_row[key])
                }
            }

        },
        getRows:function(){
            /*
            以后都用这个函数，不用什么get_data 或者 data_getter 了
            * */
            var self=this

            cfg.show_load()
            self.rows=[]

            var post_data=[{fun:'get_rows',director_name:self.director_name,search_args:self.search_args}]
            ex.post('/d/ajax',JSON.stringify(post_data),function(resp){

                self.rows = resp.get_rows.rows
                self.row_pages = resp.get_rows.row_pages
                //self.search_args=resp.get_rows.search_args
                ex.vueAssign(self.search_args,resp.get_rows.search_args)
                self.footer=resp.get_rows.footer
                self.parents=resp.get_rows.parents
                self.table_layout=resp.get_rows.table_layout
                cfg.hide_load()
            })
        },
        get_page: function (page_number) {
            this.search_args._page = page_number
            this.getRows()
        },
        get_search_args: function () {
            return this.search_args
        },
        //data_getter:function(){
        //    // 默认的 data_getter
        //    var self=this
        //
        //    cfg.show_load()
        //    var post_data=[{fun:'get_rows',director_name:this.director_name,search_args:this.search_args}]
        //    $.get('/d/ajax',JSON.stringify(post_data),function(resp){
        //        self.rows = resp.rows
        //        self.row_pages = resp.row_pages
        //        cfg.hide_load()
        //    })
        //},
        save_rows:function(rows){
            var self=this
            var post_data=[{fun:'save_rows',rows:rows}]
            cfg.show_load()
            ex.post('/d/ajax',JSON.stringify(post_data),function(resp){
                ex.each(rows,function(row){
                    var new_row = ex.findone( resp.save_rows,{pk:row.pk})
                    ex.assign(row,new_row)
                })
                cfg.hide_load(2000)
            })
        },
        clear: function () {
            this.rows = []
            this.row_pages = {}
        },

        del_selected:function(){
            var self=this
            layer.confirm('真的删除吗?', {icon: 3, title:'确认'}, function(index) {
                layer.close(index);
                //var ss = layer.load(2);
                cfg.show_load()
                var post_data = [{fun: 'del_rows', rows: self.selected}]
                ex.post('/d/ajax', JSON.stringify(post_data), function (resp) {
                    //self.row_pages.total -= self.selected.length
                    //ex.each(self.selected,function(item){
                    //    ex.remove(self.rows,{pk:item.pk} )
                    //})
                    //self.selected=[]
                    cfg.hide_load(500)
                    self.search()
                    //layer.msg('删除成功',{time:2000})
                })
            })
        },
        get_attr:function(name){
            if(name == undefined){
                return false
            }
            if(name.startsWith('!')){
                name=name.slice(1)
                name= name.trim()
                return !this[name]
            }else{
                name= name.trim()
                return this[name]
            }
        },
        //has_select:function(){
        //    return this.selected.length > 0
        //}

    }
}

var row_match={
    one_row:function(self,head){
        if(self.selected.length !=1){
            cfg.showMsg('请选择一行数据！')
            return false
        }else{
            return true
        }
    },
    many_row:function(self,head){
        if(self.selected.length ==0 ){
            cfg.showMsg('请至少选择一行数据！')
            return false
        }else{
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
    many_row_match:function(self,head){
        // head : @match_field , @match_values ,@match_msg
        if(self.selected.length ==0 ){
            cfg.showMsg('请至少选择一行数据！')
            return false
        }else{
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
        }
    },
}

function swap(arr,k,j) {
    var c = arr[k];
    arr.splice(k,1,arr[j])
    arr.splice(j,1,c)
    //arr[k] = arr[j];
    //arr[j] = c;
    return arr
}

window.mix_table_data = mix_table_data