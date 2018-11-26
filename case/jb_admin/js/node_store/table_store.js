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
         }
    },
    mixins:[mix_ele_table_adapter],
    computed:{
        changed:function(){
            return this.changed_rows.length != 0
        },
        has_select:function(){
            return this.selected.length !=0
        },
    },
    methods:{
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
            self.rows=[]

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
                if(self.search_args._par){
                    crt_row.meta_par=self.search_args._par
                }
                //var pop_id= new Date().getTime()
                // e = {name:'after_save',new_row:event.new_row,old_row:event.old_row}
                //eventBus.$on('pop-win-'+pop_id,function(e){
                //    self.update_or_insert(e.new_row, e.old_row)
                //})
                //pop_fields_layer(new_row,kws.heads,kws.ops,pop_id)
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
                            ex.eval(kws.after_save,self)
                        }
                    })
                }
            })
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

            if(old_row && ! old_row.pk) {

                //var rows = this.rows.splice(0, 0, new_row)
                this.rows=[new_row].concat(this.rows)
                this.row_pages.total+=1
            }else{
                var table_row = ex.findone(this.rows,{pk:new_row.pk})
                ex.vueAssign(table_row,new_row)
                //ex.assign(table_row,new_row)
                //for(var key in new_row){
                //    Vue.set(table_row,key,new_row[key])
                //}
            }
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
        selected_set_and_save:function(kws){
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

            function  bb(all_set_dict,after_save_callback){
                var cache_rows = ex.copy(self.selected)
                ex.each(cache_rows ,function(row){
                    ex.assign(row,all_set_dict)
                    if(kws.fields_ctx && kws.fields_ctx.director_name){
                        row._cache_director_name = row._director_name // [1] 有可能是用的特殊的 direcotor
                        row._director_name=kws.fields_ctx.director_name
                    }
                    //row[kws.field]=kws.value
                })
                var post_data=[{fun:'save_rows',rows:cache_rows}]
                cfg.show_load()
                ex.post('/d/ajax',JSON.stringify(post_data),function(resp){
                    if( !resp.save_rows.errors){
                        ex.each(resp.save_rows,function(new_row){
                            delete new_row._director_name  // [1]  这里还原回去
                            self.update_or_insert(new_row)
                        })
                        self.clearSelection()

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

            //row[kws.field]=kws.value

            function judge_pop_fun(){
                var one_row={}
                if(kws.field){ // 兼容老的，新的采用eval形式，
                    one_row[kws.field]=kws.value
                }else{
                    ex.assign(one_row,ex.eval(kws.pre_set))
                }

                if(kws.fields_ctx){
                    ex.map(kws.fields_ctx.heads,function(head){
                        if(!head.name.startsWith('_') && one_row[head.name]==undefined){
                            one_row[head.name]=self.selected[0][head.name]
                        }
                    })
                    var win_index = pop_edit_local(one_row,kws.fields_ctx,function(new_row,store){
                        bb(new_row,function(resp){
                            if(resp.save_rows.errors){
                                store.showError(resp.save_rows.errors)
                                //self.$store.commit(store_id+'/showErrors',resp.save_rows.errors)
                            }else{
                                layer.close(win_index)
                            }

                        })
                    })
                }else{
                    bb(one_row)
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

            function bb(){
                cfg.show_load()
                ex.director_call(kws.director_name,{rows:self.selected,},function(resp){
                    if(!resp.msg){
                        cfg.hide_load(2000)
                    }else{
                        cfg.hide_load()
                    }
                    if(resp.msg){
                        cfg.showMsg(resp.msg)
                    }

                    // 返回rows ，默认更新
                    if(resp.rows){
                       self.update_rows(resp.rows)
                    }
                    if(resp.row){
                        self.update_or_insert(resp.row)
                    }
                    self.clearSelection()
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
        arraySpanMethod:function({ row, column, rowIndex, columnIndex }){
            if(this.table_layout){
                return this.table_layout[`${rowIndex},${columnIndex}`] || [1,1]
            }else{
                return [1,1]
            }
        }
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

window.table_store= table_store