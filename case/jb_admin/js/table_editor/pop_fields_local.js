export  var pop_fields={
    template:`<div class="com-table-pop-fields-local">
        <span  @click="edit_me()" class="clickable">
        <component v-if="head.inn_editor" :is="head.inn_editor" :rowData="rowData" :field="field" :index="index"></component>
         <span v-else v-text="show_text"></span>
         </span>
    </div>`,
    props:['rowData','field','index'],
    created:function(){
        // find head from parent table
        var table_par = this.$parent
        while (true){
            if (table_par.heads){
                break
            }
            table_par = table_par.$parent
            if(!table_par){
                break
            }
        }
        this.table_par = table_par
        if(table_par){
            var value = this.rowData[this.field]
            this.head  = ex.findone(table_par.heads,{name:this.field})
        }
    },
    data(){
        return {
            parStore : ex.vueParStore(this)
        }
    },
    computed:{
        show_text:function(){
            if(this.head.show_label){
                return show_label[this.head.show_label.fun](this.rowData,this.head.show_label)
            }else {
                return this.rowData[this.field]
            }
        }
    },
    methods:{
        edit_me:function(){
            this.open_layer()
        },
        open_layer:function(){
            var self=this
            var fields_ctx={
                heads:self.table_par.head.fields_heads,
                ops:[{
                    'name':'save','editor':'com-field-op-btn','label':'确定', 'icon': 'fa-save',
                }],
                extra_mixin:[],
                genVc:self,
            }

               var win= pop_edit_local(self.rowData,fields_ctx,(resp)=> {
                   //ex.assign(self.rowData,resp.row)
                   ex.vueAssign(self.rowData,resp.row)
                    //self.$emit('on-custom-comp',{fun:'edit_over'} )
                   layer.close(win)
                   if(resp.row && this.head.after_save_express){
                       ex.eval(this.head.after_save_express,{vc:this})
                   }
                })

        }

    }
}
Vue.component('com-table-pop-fields-local',pop_fields)

var show_label={
    use_other_field:function(row,kws){
        var other_field=kws.other_field
        return row[other_field]
    },
    text_label:function(row,show_label){
        return show_label.text
    }
}
