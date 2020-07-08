<template>
    <div class="com-block-title-plain">
        <div class="title"  v-text="ctx.title"></div>
        <span class="sub-title"  v-text="ctx.sub_title"></span>
        <div>
            <div style="width: 50px;border-bottom: 2px solid #0aa938;display: inline-block;padding-top: 8px"></div>
        </div>

    </div>
</template>
<script>
    export default {
        props:['ctx'],
        data(){
            return {
            }
        }
    }
</script>
<style lang="scss" scoped>
.title{
    font-weight: bold;
    font-size: 130%;
    padding: 8px;
}
    .sub-title{
        color: #979797;
        font-size: 80%;
    }
</style>