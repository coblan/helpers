
var money_shower = {
    props:['rowData','field','index'],
    template:`<div v-text="rowData[field]" :style="my_style"></div>`,
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
        this.head  = ex.findone(this.table_par.heads,{name:this.field})
    },
    computed:{
        my_style:function(){
            return ex.eval(this.head.style_express,{row:this.rowData})
        }
    }
}

Vue.component('com-table-style-block',money_shower)
