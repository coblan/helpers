Vue.component('com-table-span',{
    props:['head','row'],
    template:`<span class="com-item-span" :class="head.class" v-text="row[head.name]" @click="on_click()"></span>`,
    data(){
        var parStore = ex.vueParStore(this)
        return {
            parStore:parStore
        }
    },
    mounted(){
        if(this.head.css){
            ex.append_css(this.head.css)
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