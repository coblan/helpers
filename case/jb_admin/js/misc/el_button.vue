<template>
    <span class="com-btn">
        <el-button size="mini" :type="my_ctx.type" @click="on_click()">
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
        mounted(){

        },
        methods:{
            on_click(){
                debugger
                if(this.ctx.action){
                    ex.eval(this.ctx.action,{head:this.ctx,ps:this.parStore})
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