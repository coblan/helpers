var op_a = {
    props:['head','disabled'],
    template:`<button :class="norm_class"  :style="head.style" :disabled="disabled" @click="operation_call">
        <i v-if="head.icon" :class='["fa",head.icon]'></i>
        <span  v-text="head.label"></span>
    </button>`,
    data:function(){
        return {
            enable:true
        }
    },
    computed:{
        norm_class:function(){
            if(this.head.class){
                return 'btn btn-sm '+this.head.class
            }else{
                return 'btn btn-sm btn-default'
            }
        }
    },
    methods:{
        operation_call:function(){
            this.$emit('operation',this.head)
        },
        set_enable:function(yes){
            this.enable= yes
        }
    }
}
Vue.component('com-op-plain-btn',op_a)