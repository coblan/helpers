Vue.component('com-table-span',{
    props:['head','row'],
    template:`<span class="com-item-span" v-text="row[head.name]" @click="on_click()"></span>`,
    data(){
        var parStore = ex.vueParStore(this)
        return {
            parStore:parStore
        }
    },
    methods:{
        on_click(){
            if(this.head.action){
                ex.eval(this.head.action,{head:this.head,row:this.row,ps:this.parStore})
            }
        }
    }
})