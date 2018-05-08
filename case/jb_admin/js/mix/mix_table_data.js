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
            //get_data:function(){
            //    self.getRows()
            //},
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
            var post_data=[{fun:'get_row',model_name:fields_ctx.model_name},]
            cfg.show_load()
            ex.post('/d/ajax',JSON.stringify(post_data),function(resp){
                cfg.hide_load()
                var new_row = resp.get_row
                //var pop_id= new Date().getTime()
                // e = {name:'after_save',new_row:event.new_row,old_row:event.old_row}
                //eventBus.$on('pop-win-'+pop_id,function(e){
                //    self.update_or_insert(e.new_row, e.old_row)
                //})
                //pop_fields_layer(new_row,kws.heads,kws.ops,pop_id)
                pop_fields_layer(new_row,fields_ctx.heads,fields_ctx.ops,fields_ctx.extra_mixins,function(e){
                    self.update_or_insert(e.new_row, e.old_row)
                })
            })
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
            var post_data=[{fun:'get_rows',model_name:self.model_name,search_args:self.search_args}]
            $.post('/d/ajax',JSON.stringify(post_data),function(resp){
                self.rows = resp.get_rows.rows
                self.row_pages = resp.get_rows.row_pages
                cfg.hide_load()
            })
        },
        get_data: function () {
            this.data_getter(this)
        },
        get_page: function (page_number) {
            this.search_args._page = page_number
            this.getRows()
        },
        get_search_args: function () {
            return this.search_args
        },
        data_getter:function(){
            // 默认的 data_getter
            var self=this

            cfg.show_load()
            var post_data=[{fun:'get_rows',model_name:this.model_name,search_args:this.search_args}]
            $.get('/d/ajax',JSON.stringify(post_data),function(resp){
                self.rows = resp.rows
                self.row_pages = resp.row_pages
                cfg.hide_load()
            })
        },
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

        //del_item: function () {
        //    if (this.selected.length == 0) {
        //        return
        //    }
        //    var del_obj = {}
        //    for (var j = 0; j < this.selected.length; j++) {
        //        var pk = this.selected[j]
        //        for (var i = 0; i < this.rows.length; i++) {
        //            if (this.rows[i].pk.toString() == pk) {
        //                if (!del_obj[this.rows[i]._class]) {
        //                    del_obj[this.rows[i]._class] = []
        //                }
        //                del_obj[this.rows[i]._class].push(pk)
        //            }
        //        }
        //    }
        //    var out_str = ''
        //    for (var key in del_obj) {
        //        out_str += (key + ':' + del_obj[key].join(':') + ',')
        //    }
        //    location = ex.template("{engine_url}/del_rows?rows={rows}&next={next}", {
        //        engine_url: engine_url,
        //        rows: encodeURI(out_str),
        //        next: encodeURIComponent(location.href)
        //    })
        //},
        //goto_page: function (page) {
        //    this.search_args._page = page
        //    this.get_data()
        //},
        //add_new: function () {
        //    var url = ex.template('{engine_url}/{page}.edit/?next={next}', {
        //        engine_url: engine_url,
        //        page: page_name,
        //        next: encodeURIComponent(ex.appendSearch(location.pathname, search_args))
        //    })
        //    location = url
        //},
    }
}

window.mix_table_data = mix_table_data