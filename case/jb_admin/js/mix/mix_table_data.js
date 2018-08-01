var mix_table_data={
    data:function(){
        return {
            op_funs:{},
            changed_rows:[]
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
            emitEvent:function(e){
                self.$emit(e)
            },
            // 为了刷新界面，付出了清空的代价，这两个函数小心使用，
            row_up:function(kws){
                var row=kws.row
                var index =self.rows.indexOf(row)
                if(index >=1 ){
                    var ss = swap(self.rows,index-1,index)
                    self.rows=[]
                    Vue.nextTick(function(){
                        self.rows=ss
                    })

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
                    self.rows=[]
                    Vue.nextTick(function(){
                        self.rows=ss
                    })
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
        }
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
            var post_data=[{fun:'get_row',director_name:fields_ctx.director_name},]
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
                pop_fields_layer(crt_row,fields_ctx,function(new_row){
                    self.update_or_insert(new_row, crt_row)
                })
            })
        },
        editRow:function(kws){
            var row=kws.row
            var fields_ctx = kws.fields_ctx

        },
        update_or_insert:function(new_row,old_row){
            if(old_row && ! old_row.pk) {
                this.rows.splice(0, 0, new_row)
            }else{
                var table_row = ex.findone(this.rows,{pk:new_row.pk})
                ex.assign(table_row,new_row)
            }
        },
        getRows:function(){
            /*
            以后都用这个函数，不用什么get_data 或者 data_getter 了
            * */
            var self=this

            cfg.show_load()
            var post_data=[{fun:'get_rows',director_name:self.director_name,search_args:self.search_args}]
            $.post('/d/ajax',JSON.stringify(post_data),function(resp){
                self.rows = resp.get_rows.rows
                self.row_pages = resp.get_rows.row_pages
                self.search_args=resp.get_rows.search_args
                cfg.hide_load()
            })
        },
        get_data: function () {
            this.getRows()
            //this.data_getter(this)
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
                $.post('/d/ajax', JSON.stringify(post_data), function (resp) {
                    //layer.close(ss)
                    ex.each(self.selected,function(item){
                        ex.remove(self.rows,{pk:item.pk} )
                    })
                    self.selected=[]
                    cfg.hide_load(200)
                    //layer.msg('删除成功',{time:2000})
                })
            })
        },

    }
}


function swap(arr,k,j) {
    var c = arr[k];

    arr[k] = arr[j];
    arr[j] = c;
    return arr
}

window.mix_table_data = mix_table_data