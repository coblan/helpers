var submit_btn = {
    props:['head'],
    template:`<van-button class="com-op-submit" :type="head.type || 'primary'" @click="on_click()" size="large">
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
            var click_express = this.head.click_express || this.head.action
            if( click_express ){
                ex.eval( click_express ,{ps:this.parStore,head:this.head,vc:this})
            }else{
                this.$emit('action')
            }

        }
    }

}

Vue.component('com-op-submit',submit_btn)
Vue.component('com-btn',submit_btn)