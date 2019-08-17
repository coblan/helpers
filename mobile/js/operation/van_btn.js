require('./styl/van_btn.styl')

Vue.component('com-op-van-btn',{
    props:['head'],
    template:`<van-button class="com-op-van-btn" com-op-submit :type="head.type || 'primary'" @click="on_click()" size="large ">
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
            debugger
            if(this.head.action){
                ex.eval(this.head.action,{ps:this.parStore,head:this.head})
            }
        }
    }

})