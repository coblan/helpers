/*

 * */

export  var pop_table={
    template:`<span @click="open_layer()" class="clickable">
        <component v-if="head.inn_editor" :is="head.inn_editor" :rowData="rowData" :field="field" :index="index"></component>
        <span v-else v-text="show_text"  ></span>
    </span>`,
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
        if(table_par){
            var value = this.rowData[this.field]
            this.head  = ex.findone(table_par.heads,{name:this.field})
        }

    },
    computed:{
        show_text:function(){
            return this.rowData[this.field]
        }
    },
    methods:{
        async open_layer(){
            var com = await import(/* webpackChunkName: 'maybe_old' */'../table_panels/ele_table.js')
            var table_ctx=com.init_table_ctx(this.head.table_ctx)
            pop_table_layer(this.rowData,table_ctx,function(){
            })
        }

    }
}
// Vue.component('com-table-pop-table',pop_table)
