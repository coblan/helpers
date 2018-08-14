
var money_shower = {
    props:['rowData','field','index'],
    template:`<span v-text="show_text" ></span>`,
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
    },

    computed:{
        show_text:function(){
            if(this.rowData[this.field]){
                return parseFloat( this.rowData[this.field]) .toFixed(this.head.digit)
            }else{
                return this.rowData[this.field]
            }

        }
    }


}

Vue.component('com-table-digit-shower',money_shower)
