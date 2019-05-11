
var html_shower = {
    props:['rowData','field','index'],
    template:`<span v-html="rowData[field]"></span>`,
    created(){
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
    },
    mounted(){

    }

}

Vue.component('com-table-html-shower',html_shower)


