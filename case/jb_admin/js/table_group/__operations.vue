<template>
    <div class="com-table-operations-pannel" style="padding: 5px;overflow: hidden;flex-shrink: 0;">
        <component v-for="(op,index) in ops"
                   :is="op.editor"
                   :ref="'op_'+op.name"
                   :head="op"
                   :ctx="op"
                   :key="index"
                   :disabled="is_disable(op)"
                   v-show="is_show(op)"
                   @operation="on_operation(op)"></component>
    </div>
</template>
<script>
//    新的table-operations控件,对接
    export default {
        data(){
            var self = this
            this.parStore = ex.vueParStore(this)
            return {
                ops: this.parStore.ops,
            }
        },
        methods: {
            is_disable: function (op) {
                if (op.disabled == undefined) {
                    return false
                } else {
                    return ex.eval(op.disabled, {ps: this.parStore})
                }

            },
            is_show: function (op) {
                count += 1
                console.log(count)
                console.log(op.label)
                if (op.show == undefined) {
                    return true
                } else {
                    return ex.eval(op.show, {ps: this.parStore})
                }
            },
            eval: function (express) {
                if (express == undefined) {
                    return false
                } else {
                    return ex.eval(express, this.parStore)
                }
            },
            on_operation: function (op) {
                var fun_name = op.fun || op.name  // 以后都使用 fun
                this.parStore[fun_name](op)
            }
        }
    }
</script>
