var ele_operations={

    //                      :disabled="get_attr(op.disabled)"
    //v-show="! get_attr(op.hide)"
    template:`<div class="oprations" style="padding: 5px;">
                <component v-for="op in ops"
                           :is="op.editor"
                           :ref="'op_'+op.name"
                           :head="op"
                           :disabled="eval(op.disabled)"
                           v-show="op.show==undefined?true:eval(op.show)"
                           @operation="on_operation(op)"></component>
            </div>`,
    data:function(){
        var self = this
        this.parStore = ex.vueParStore(this)
        return {
            ops:this.parStore.ops,
        }
    },
    methods:{
        eval:function (express){
            if(express ==undefined){
                return false
            }else{
                return ex.eval(express,this.parStore)
            }
        },
        on_operation:function(op){
            var fun_name =  op.fun || op.name  // 以后都使用 fun
            this.parStore[fun_name](op)
            //this.bus.eventBus.$emit('operation',op)
        }
    }
}

Vue.component('com-table-operations',ele_operations)