
var switch_to_tab = {
    props:['rowData','field','index'],
    template:`<span @click="goto_tab()" class="clickable">
     <component v-if="head.inn_editor" :is="head.inn_editor" :rowData="rowData" :field="field" :index="index"></component>
    <span v-else v-text="rowData[field]"></span>
    </span>`,
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
        var head  = ex.findone(table_par.heads,{name:this.field})
        this.head = head
    },
    methods:{
        goto_tab:function(){
            if(this.head.tab_name_express){
                var tab_name = ex.eval(this.head.tab_name_express,{par_row:this.rowData,head:this.head})
            }else{
                var tab_name = this.head.tab_name
            }
            if(this.head.ctx_name_express){
                var ctx_name = ex.eval(this.head.ctx_name_express,{par_row:this.rowData,head:this.head})
            }else{
                var ctx_name = this.head.ctx_name
            }

            this.$emit('on-custom-comp',
                {
                    fun:'switch_to_tab',
                    tab_name:tab_name,
                    ctx_name:ctx_name ,
                    named_tabs:this.head.named_tabs, // 准备淘汰
                    par_row:this.rowData
                }
            )
        }
    }
}

Vue.component('com-table-switch-to-tab',switch_to_tab)
