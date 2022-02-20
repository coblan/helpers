
var label_shower = {
    props:['rowData','field','index'],
    template:`<span class="table-span ellipsis" v-text="show_text" @click="on_click()"></span>`,
    computed:{
        show_text:function(){
            var value = this.rowData[this.field]
            if( value == undefined){
                return ''
            }else if(typeof value == 'object'){
                return JSON.stringify(value)
            } else{
                return this.rowData[this.field]
            }
        }
    },
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
            if(this.head.click_express){
                ex.eval(this.head.click_express,{row:this.rowData,head:this.head,ps:this.parStore})
            }
        }
    }
}

Vue.component('com-table-span',label_shower)
