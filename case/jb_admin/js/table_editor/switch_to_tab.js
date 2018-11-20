
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
            this.$emit('on-custom-comp',
                {
                    fun:'switch_to_tab',
                    tab_name:this.head.tab_name,
                    named_tabs:this.head.named_tabs,
                    row:this.rowData
                }
            )
            //eventBus.$emit('switch_to_tab',
            //    {
            //        name:'switch_to_tab',
            //        tab_name:this.head.tab_name,
            //        named_tabs:this.head.named_tabs,
            //        row:this.rowData
            //    })

        }
    }
}

Vue.component('com-table-switch-to-tab',switch_to_tab)
