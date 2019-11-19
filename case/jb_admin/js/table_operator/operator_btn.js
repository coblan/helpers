var op_a = {
    props:['head','disabled'],
    template:` <span class="com-op-btn" style="margin-left: 3px">
    <button :class="norm_class" @click="operation_call()"  :style="head.style" :disabled="disabled">
        <i v-if="head.icon" :class='["fa",head.icon]'></i>
        <span  v-text="head.label"></span>
    </button>
    </span>`,
    data:function(){
        var parStore = ex.vueParStore(this)
        return {
            enable:true,
            parStore : parStore,
        }
    },
    mounted(){
        if(this.head.css){
            ex.append_css(this.head.css)
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
            if (this.head.action) {
                if(this.head.row_match && !this.parStore.check_selected(this.head)){
                    return
                }
                if(this.head.confirm_msg){
                    cfg.confirm(this.head.confirm_msg).then(()=>{
                        ex.eval(this.head.action, {ps: this.parStore, head: this.head,self:this})
                    })
                }else{
                    ex.eval(this.head.action, {ps: this.parStore, head: this.head,self:this})
                }

            }else{
                this.$emit('operation',this.head.name || this.head.fun)
            }
        },
        set_enable:function(yes){
            this.enable= yes
        }
    }
}
Vue.component('com-op-btn',op_a)