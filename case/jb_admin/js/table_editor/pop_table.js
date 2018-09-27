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
            if(this.head.show_label){
                return show_label[this.head.show_label.fun](this.rowData,this.head.show_label)
            }else {
                return this.rowData[this.field]
            }
        }
    },
    methods:{
        open_layer:function(){
            var table_ctx=init_table_ctx(this.head.table_ctx)
            pop_table_layer(this.rowData,table_ctx,function(){
            })
        }

    }
}
Vue.component('com-table-pop-fields',pop_fields)
