
var bool_shower = {
    props:['rowData','field','index'],
    template:`<span>
    <a :href="link" target="_blank" v-text="rowData[field]"></a>
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
        this.table_par = table_par
        this. head  = ex.findone(this.table_par.heads,{name:this.field})
    },
    computed:{
        link:function(){
            return this.rowData[this.head.link_field]
        }
    }

}

Vue.component('com-table-jump-link',bool_shower)

