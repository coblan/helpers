
var my_click = {
    // head: {fun:'xxx'}
    props:['rowData','field','index'],
    template:`<span v-text="rowData[field]" class="clickable" @click="on_click()"></span>`,
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

        this.parStore = ex.vueParStore(this)
    },
    methods:{
        on_click:function(){
            ex.eval(this.head.action,{row:this.rowData,head:this.head,ps:this.parStore})
            //this.$emit('on-custom-comp',{name:this.head.fun,row:this.rowData,head:this.head})
        }
    }
}

Vue.component('com-table-click',my_click)
