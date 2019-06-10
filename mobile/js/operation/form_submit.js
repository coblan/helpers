var submit_btn = {
    props:['head'],
    template:`<van-button com-op-submit type="primary" @click="on_click()" size="large">
            <span v-text="head.label || '确定'"></span>
        </van-button>`,
    data:function(){
        let parStore = ex.vueParStore(this)
        return {
            parStore:parStore
        }
    },
    methods:{
        on_click:function(){
            if(this.head.action){
                ex.eval(this.head.action,{ps:this.parStore})
            }else{
                this.$emit('action')
            }

        }
    }

}

Vue.component('com-op-submit',submit_btn)