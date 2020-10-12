//require('./scss/tab_fields.scss')
require('./scss/form_one.scss')
export  var fields_all_in_one={
    props:['ctx'],
    data:function(){
        if (this.ctx.director_name){
            var def_row = {_director_name:this.ctx.director_name}
        }else{
            var def_row = {}
        }
        var data_row = ex.copy(this.ctx.row  || def_row )
        var self=this
        var childStore = new Vue({
            data:{
                vc:self
            }
        })
        var parStore = ex.vueParStore(this)
        return {
            head:this.ctx,
            par_row:this.ctx.par_row,
            heads:this.ctx.heads,
            //layout:this.ctx.layout,
            fields_group:this.ctx.fields_group,
            table_grid:this.ctx.table_grid,
            ops:this.ctx.ops,
            errors:{},
            row:data_row,
            org_row:data_row,
            childStore:childStore,
            parStore:parStore,
            ops_loc: this.ctx.ops_loc ||  'up'
        }
    },
    mixins:[mix_fields_data,mix_nice_validator],
    template:`<div class="com-form-one flex-v" :class="head.class">
   <div class="oprations" v-if="ops_loc=='up'">
        <component v-for="op in ops" :is="op.editor" :ref="'op_'+op.name" :ctx="op" :head="op" @operation="on_operation(op)"></component>
    </div>
    <div style="overflow: auto;" class="flex-grow fields-area">
            <!--有分组的情况-->
           <div v-if="fields_group" >
                <div v-for="group in grouped_heads_bucket" :class="'group_'+group.name" v-if="group.heads.length > 0">

                         <div class="fields-group-title"  v-html="group.label"></div>
                        <com-fields-table-block v-if="table_grid "
                            :heads="group.heads" :row="row" :option="{table_grid:table_grid}">
                         </com-fields-table-block>
                         <div v-else class='field-panel suit' >
                            <field  v-for='head in group.heads' :key="head.name" :head="head" :row='row'></field>
                        </div>
                </div>
        </div>
        <!--只有table分组-->
         <div v-else-if="table_grid " >
                    <com-fields-table-block
                        :heads="normed_heads" :row="row" :option="{table_grid:table_grid}"></com-fields-table-block>
         </div>
         <!--没有分组-->
        <div v-else class='field-panel suit' id="form" >
            <field  v-for='head in normed_heads' :key="head.name" :head="head" :row='row'></field>
        </div>
    </div>
    <div class="oprations bottom" v-if="ops_loc=='bottom'">
        <component v-for="op in normed_ops" :key="op.name" :is="op.editor" :ref="'op_'+op.name" :head="op" :ctx="op" @operation="on_operation(op)"></component>
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
    computed:{
        normed_ops(){
            return ex.filter(this.ops,(op)=>{
                if(op.show){
                    return ex.eval(op.show,{row:this.row,vc:this})
                }else{
                    return true
                }
            })
        },
        grouped_heads_bucket:function(){
            var out_bucket = []
            ex.each(this.fields_group,(group)=>{
                if(group.show && ! ex.eval(group.show,{row:this.row,head:this.head})){
                    return
                }
                var heads = ex.filter(this.normed_heads,function(head){
                    return ex.isin(head.name,group.heads)
                })
                out_bucket.push({name:group.name,label:group.label,heads:heads})
            })
            return out_bucket

        }
    },

    methods:{
        group_filter_heads:function(group){
            return ex.filter(this.normed_heads,function(head){
                return ex.isin(head.name,group.heads)
            })
        },
        data_getter:function(){
            var self=this
            if(self.tab_head.get_data){
                var fun = get_data [self.tab_head.get_data.fun]
                var kws = self.tab_head.get_data.kws
                fun(self,function(row){
                    self.org_row = row
                    self.row = ex.copy(row)
                    self.childStore.$emit('row.update_or_insert',row)
                },kws)
            }
            if(self.tab_head.get_row){
                ex.eval(self.tab_head.get_row,{vc:self})
            }
        },
        save(){
            if(this.head.save_express){
                return ex.eval(this.head.save_express,{vc:this})
            }else{
                return  mix_fields_data.methods.save.call(this)
            }
        }
    }
    // data_getter  回调函数，获取数据,


}

Vue.component('com-form-one',fields_all_in_one)

var get_data={
    get_row:function(self,callback,kws){
        //kws={model_name ,relat_field}
        var director_name = kws.director_name
        var relat_field = kws.relat_field
        var dt = {fun:'get_row',director_name:director_name}
        dt[relat_field] = self.par_row[relat_field]
        //var post_data=[dt]
        cfg.show_load()
        ex.director_call('d.get_row?dname='+director_name,dt).then((resp)=>{
            cfg.hide_load()
            callback(resp)
        })

        //$.post('/d/ajax',JSON.stringify(post_data),function(resp){
        //    cfg.hide_load()
        //    callback(resp.get_row)
        //})
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