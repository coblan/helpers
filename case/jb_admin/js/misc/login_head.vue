<template>
    <div class="com-ui-login-head">
        <h2 class='form-signin-heading' v-text="ctx.title"></h2>
        <div style="position: relative">
            <hr>
        <div class="sub-title" v-text="ctx.subtitle"></div>
        </div>
    </div>

</template>
<script>
export default {
    props:['ctx']
}
</script>
<style lang="scss" scoped>
.form-signin-heading{
    text-align: center;
    margin-bottom: 1em;
}
    .sub-title{
        position: absolute;
        top:50%;
        left:50%;
        transform: translate(-50%,-50%);
        background-color:white;
        padding: 0 1em;
        /*width: 12em;*/
        white-space: nowrap;
    }
</style>