Vue.component('com-field-op-btn',{
    props:['head'],
    template:`<div class="com-field-op-btn" style="display: inline-block;margin: 0 3px">
    <button @click="operation_call()" :class="head.class?head.class:'btn btn-default'">
        <i v-if="head.icon" :class="['fa',head.icon]"></i><span style="display: inline-block;margin-left: 5px" v-text="head.label"></span>
        </button>
    </div>`,
    methods:{
        operation_call:function(){
            this.$emit('operation',this.head.name)
        },
    }
})