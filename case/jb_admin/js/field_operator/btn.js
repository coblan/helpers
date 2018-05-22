Vue.component('com-field-op-btn',{
    props:['head'],
    template:`<button @click="operation_call()" class="btn btn-default">
        <i v-if="head.icon" :class="['fa',head.icon]"></i><span v-text="head.label"></span>
        </button>`,
    methods:{
        operation_call:function(){
            this.$emit('operation',this.head.name)
        },
    }
})