/*
将数据  [1,2,3,4]   显示为 1;2;3;4

 * */
var array_mapper = {
    props:['rowData','field','index'],
    template:`<span v-text="show_data"></span>`,
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
        this.head = ex.findone(this.table_par.heads,{name:this.field})
    },
    computed:{
        show_data:function(){
            if(this.rowData[this.field]){
                return this.rowData[this.field].join(';')
            }else{
                return ''
            }
        },

    }
}



Vue.component('com-table-array-shower',array_mapper)
