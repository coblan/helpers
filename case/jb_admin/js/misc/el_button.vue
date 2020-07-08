<template>
    <span class="com-btn">
        <el-button size="small" :type="ctx.type" @click="on_click()">
            <slot name="content">
                <i v-if="ctx.icon" :class="ctx.icon"></i>
                <span v-text="ctx.label"></span>
            </slot>
        </el-button>
    </span>
</template>
<script>
    export default {
        props:['ctx'],
        data(){
            return {
                parStore:ex.vueParStore(this)
            }
        },
        mounted(){

        },
        methods:{
            on_click(){
                if(this.ctx.action){
                    ex.eval(this.ctx.action,{head:this.ctx,ps:this.parStore})
                }
            }
        }
    }
</script>

<style scoped lang="scss">
.com-btn{
    margin: 0 2px;
}
</style>