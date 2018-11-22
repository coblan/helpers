require('./scss/tab_fields.scss')

var tab_fields={
    props:['tab_head','par_row'],
    data:function(){
        var data_row = this.tab_head.row || {}
        return {
            heads:this.tab_head.heads,
            ops:this.tab_head.ops,
            errors:{},
            row:data_row,
        }
    },
    mixins:[mix_fields_data,mix_nice_validator],
    template:`<div class="com-tab-fields flex-v"  style="position: absolute;top:0;left:0;bottom: 0;right:0;overflow: auto;">

   <div class="oprations" >
        <component v-for="op in ops" :is="op.editor" :ref="'op_'+op.name" :head="op" @operation="on_operation(op)"></component>
    </div>
    <div style="overflow: auto;" class="flex-grow">
        <div class='field-panel suit' id="form" >
            <field  v-for='head in normed_heads' :key="head.name" :head="head" :row='row'></field>
        </div>
    </div>
    </div>`,

    //created:function(){
    //    // find head from parent table
    //    var table_par = this.$parent
    //    while (true){
    //        if (table_par.heads){
    //            break
    //        }
    //        table_par = table_par.$parent
    //        if(!table_par){
    //            break
    //        }
    //    }
    //    this.table_par = table_par
    //},

    mounted:function(){
        if(!this.tab_head.row){
            this.get_data()
        }
    },
    methods:{

        data_getter:function(){
            var self=this
            var fun = get_data [self.tab_head.get_data.fun]
            var kws = self.tab_head.get_data.kws
            fun(self,function(row){
                //ex.assign(self.row,row)
                self.row = row
            },kws)

            //var self=this
            //cfg.show_load()
            //var dt = {fun:'get_row',model_name:this.model_name}
            //dt[this.relat_field] = this.par_row[this.relat_field]
            //var post_data=[dt]
            //$.post('/d/ajax',JSON.stringify(post_data),function(resp){
            //    self.row=resp.get_row
            //    cfg.hide_load()
            //})
        },
        after_save:function(new_row){
            if(this.tab_head.after_save){
                var fun = after_save[this.tab_head.after_save.fun]
                var kws = this.tab_head.after_save.kws
                // new_row ,old_row
                fun(this,new_row,kws)

                //if(  self.par_row._director_name == row._director_name){
                //    // ，应该将新的属性值 去更新par_row
                //    ex.vueAssign(self.par_row,row)
                //}
            }
            this.row=new_row
        }
    }
    // data_getter  回调函数，获取数据,


}

Vue.component('com-tab-fields',tab_fields)

var get_data={
    get_row:function(self,callback,kws){
        //kws={model_name ,relat_field}
        var director_name = kws.director_name
        var relat_field = kws.relat_field
        var dt = {fun:'get_row',director_name:director_name}
        dt[relat_field] = self.par_row[relat_field]
        var post_data=[dt]
        cfg.show_load()
        $.post('/d/ajax',JSON.stringify(post_data),function(resp){
            cfg.hide_load()
            callback(resp.get_row)
        })
    },
    table_row:function(self,callback,kws){
        callback(self.par_row)
    }
}

var after_save={
    update_or_insert:function(self,new_row,kws){
        var old_row= self.old_row
        var parStore = ex.vueParStore(self)
        parStore.update_or_insert(new_row,old_row)
        // 要update_or_insert ，证明一定是 更新了 par_row
        //ex.vueAssign(self.par_row,new_row)
        //self.$emit('tab-event',{name:'update_or_insert',new_row:self.par_row,old_row:old_row})
    },
    do_nothing:function(self,new_row,kws){
    },

    update_par_row_from_db:function(self,new_row,kws){
        //
        var post_data=[{fun:'get_row',director_name:self.par_row._director_name,pk:self.par_row.pk}]
        ex.post('/d/ajax',JSON.stringify(post_data),function(resp){
            ex.vueAssign(self.par_row,resp.get_row)
        })
    }
}