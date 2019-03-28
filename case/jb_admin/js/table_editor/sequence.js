/*
* 用于 表格最左侧的 序号显示。。。
* */
var com_table_sequence={
    props:['rowData','field','index'],
    template:`<div><span v-text="show_text" ></span></div>`,
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
        this. head  = ex.findone(this.table_par.heads,{name:this.field})
        this.parStore=ex.vueParStore(this)
    },
    computed:{
        show_text:function(){
            var perpage = this.parStore.row_pages.perpage
            var crt_page = this.parStore.row_pages.crt_page
            return this.index+1+ (crt_page-1)* perpage
        }
    }
}
Vue.component('com-table-sequence',com_table_sequence)