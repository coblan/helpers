
/*
options:{
    key:value
}
* */
var mapper = {
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
        this.head= ex.findone(this.table_par.heads,{name:this.field})
    },
    computed:{
        show_data:function(){
            if(this.table_par){
                var value = this.rowData[this.field]
                var options = this.head.options
                var opt = ex.findone(options,{value:value})
                if(opt){
                    return opt['label']
                }else{
                    return value
                }
            }

        }
    }
}

Vue.component('com-table-mapper',mapper)
