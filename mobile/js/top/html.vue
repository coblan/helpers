<template>
<div class="com-top-html" v-html="ctx.html">
</div>
</template>
<script>
export default {
    props:['ctx'],
    methods:{

    }
}
</script>
<style lang="scss">
.com-top-html{
    img{
        max-width: 100%;
        height: auto;
    }
}
</style>