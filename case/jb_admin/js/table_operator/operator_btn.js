var op_a = {
    props:['head','disabled'],
    template:` <span style="margin-left: 3px">
    <button :class="norm_class" @click="operation_call()"  :style="head.style" :disabled="disabled">
        <i v-if="head.icon" :class='["fa",head.icon]'></i>
        <span  v-text="head.label"></span>
    </button>
    </span>`,
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
            this.$emit('operation',this.head.name || this.head.fun)
        },
        set_enable:function(yes){
            this.enable= yes
        }
    }
}
Vue.component('com-op-btn',op_a)