<template>
    <div class="com-ui-login-footer" >
        <span v-text="ctx.copyright"></span>
    </div>
</template>
<script>
export default {
    props:['ctx']
}
</script>
<style lang="scss" scoped>
.com-ui-login-footer{
    text-align: center;
    position: fixed;
    bottom: 30px;
    width: 100%;
    /*position: absolute;*/
    /*bottom: -130px;*/
    /*width: 30em;*/
}
</style>