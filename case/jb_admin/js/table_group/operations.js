var ele_operations={

    //                      :disabled="get_attr(op.disabled)"
    //v-show="! get_attr(op.hide)"   // overflow: hidden  是因为有 refresh 按钮 是float:right 的；
    template:`<div class="oprations" style="padding: 5px;overflow: hidden">
                <component v-for="(op,index) in ops"
                           :is="op.editor"
                           :ref="'op_'+op.name"
                           :head="op"
                           :ctx="op"
                           :key="index"
                           :disabled="is_disable(op)"
                           v-show="is_show(op)"
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
        is_disable:function(op){
            if(op.disabled==undefined){
                return false
            }else{
                return ex.eval(op.disabled,{ps:this.parStore})
            }

        },
        is_show:function(op){
            count +=1
            console.log(count)
            console.log(op.label)
            if(op.show==undefined){
                return true
            }else{
                return ex.eval(op.show,{ps:this.parStore})
            }
        },
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

var count = 0
Vue.component('com-table-operations',ele_operations)
console.log('import operation')
import  pagination from  './pagination.vue'