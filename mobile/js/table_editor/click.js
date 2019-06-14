Vue.component('com-table-click',{
    props:['head','row'],
    template:`<span class="com-table-click" :class="head.class" v-text="row[head.name]" @click="on_click()"></span>`,
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