<template>
    <div class="com-engin-home">
        <div class="my-content">
            欢迎访问
            <span class="myblue" v-text="ctx.title"></span>
            管理后台!
        </div>
    </div>
</template>
<script>
    export default {
        props:['ctx']
    }
</script>
<style scoped lang="scss">
    .my-content{
        padding: 30px 30px;
    }
    .myblue{
        color: #357c68;
        font-weight: bold;
    }
</style>