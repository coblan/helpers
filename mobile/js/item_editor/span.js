Vue.component('com-table-span',{
    props:['head','row'],
    template:`<span class="com-item-span" :style="mystyle" :class="cssclass" v-text="row[head.name]" @click="on_click()"></span>`,
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
    computed:{
        cssclass(){
            if(this.head.class_express){
                return ex.eval(this.head.class_express,{row:this.row,head:this.head})
            }else{
                return this.head.class
            }
        },
        mystyle(){
            if(this.head.width){
                return {'width':this.head.width}
            }else{
                return {}
            }
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