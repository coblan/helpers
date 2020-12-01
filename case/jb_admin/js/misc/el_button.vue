<template>
    <span class="com-btn" :class="my_ctx.class">
        <el-button :size="my_ctx.size || 'mini' " :type="my_ctx.type" @click="on_click()"
                   :title="my_ctx.title"
                   :icon="my_ctx.icon"
                   :disabled="is_disabled"
                   :plain="my_ctx.plain"
                   :circle ="my_ctx.shape=='circle'">
            <slot name="content">
                <i v-if="my_ctx.fa_icon" :class="my_ctx.fa_icon"></i>
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
            if(this.my_ctx.css){
                ex.append_css(this.my_ctx.css)
            }
        },
        methods:{
             on_click(){
                if(this.my_ctx.click_express || this.my_ctx.action){

                    var click_express = this.my_ctx.click_express ||this.my_ctx.action
                    // 在table组件中，会先检查选中的row。
                    if(this.my_ctx.row_match){
                        var p = this.parStore.check_selected(this.my_ctx)
                    }else{
                       var p = Promise.resolve()
                    }
                    p.then(()=>{
                        ex.eval(click_express,{head:this.my_ctx,ps:this.parStore,vc:this})
                     })
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