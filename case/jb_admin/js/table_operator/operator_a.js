var op_a = {
    props:['head'],
    template:` <a class="clickable" @click="operation_call()"  :style="head.style">
    <i v-if="head.icon" :class='["fa",head.icon]'></i> <span  v-text="head.label"></span></a>`,
    data:function(){
        var parStore = ex.vueParStore(this)
        return {
            enable:true,
            parStore:parStore,
        }
    },
    methods:{
        operation_call:function(){
            if (this.head.action){
                ex.eval(this.head.action,{ps:this.parStore,head:this.head})
            }else{
                this.$emit('operation',this.head.name)
            }
        },
        set_enable:function(yes){
            this.enable= yes
        }
    }
}
Vue.component('com-op-a',op_a)