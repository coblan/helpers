
var my_link = {
    props:['rowData','field','index'],
    template:`<a class="com-table-link clickable" :href="rowData[field]" v-text="rowData[field]"></a>`,
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
    data(){
        return {
            parStore:ex.vueParStore(this)
        }
    },
    methods:{
        //on_click(){
        //    ex.eval(this.head.action,{head:this.head,row:this.rowData,ps:this.parStore})
        //}
    }
}

Vue.component('com-table-link',my_link)

