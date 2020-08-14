<template>
    <span class="com-btn" :class="my_ctx.class">
        <el-button size="mini" :type="my_ctx.type" @click="on_click()"
                   :title="ctx.title"
                   :disabled="is_disabled" :plain="my_ctx.plain">
            <slot name="content">
                <i v-if="my_ctx.icon" :class="my_ctx.icon"></i>
                <span v-text="my_ctx.label"></span>
            </slot>
        </el-button>
    </span>
</template>
<script>
    export default {
        props:['ctx','head'],
        data(){
            return {
                parStore:ex.vueParStore(this),
                // TODO 剔除某些老组件后，需要移除 head的引用
                my_ctx:this.ctx?this.ctx:this.head,
            }
        },
        computed:{
            is_disabled(){

                if(this.my_ctx .disabled){
                    return  ex.eval(this.my_ctx.disabled,{ps:this.parStore})
                }else{
                    return false
                }

            }
        },
        mounted(){
            if(this.ctx.css){
                ex.append_css(this.ctx.css)
            }
        },
        methods:{
            on_click(){
                if(this.ctx.action){
                    // 在table组件中，会先检查选中的row。
                    if(this.ctx.row_match && !this.parStore.check_selected(this.ctx)){
                        return
                    }
                    ex.eval(this.ctx.action,{head:this.ctx,ps:this.parStore,vc:this})
                }
            }
        }
    }
</script>

<style scoped lang="scss">
.com-btn{
    margin: 0 1px;
}
</style>