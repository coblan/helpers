<template>
    <div class="com-pop-progress">
        <el-progress :text-inside="true" :stroke-width="24" :percentage="ctx.ps.progress" status="success"></el-progress>
        <div class="mylabel">
            <i class="fa fa-spinner fa-spin" style="color: grey"></i>
            <span style="display: inline-block;margin-left: 10px" v-text="ctx.label"></span>
        </div>
    </div>
</template>
<script>
    export default {
        props:['ctx'],

        computed:{
            progress(v){
                return this.ctx.ps.progress
            }
        },
        watch:{
            progress(v){
                if(v>=100){
                    setTimeout(()=>{
                        this.$emit('finish',null)
                    },500)
                }
            }
        },


    }
</script>
<style lang="scss" scoped>
.com-pop-progress{
    background-color: rgba(0,0,0,0);
    height: 60px;
    width: 100%;
    padding: 20px;
    text-align: center;
}
    .mylabel{
        margin-top: 5px;
    }
</style>