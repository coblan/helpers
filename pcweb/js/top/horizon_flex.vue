<template>
    <div class="com-top-horizon-flex">
        <component :is="item.editor" v-for="item in ctx.items" :ctx="item"></component>
    </div>
</template>
<script>
    export default {
        props:['ctx']
    }
</script>
<style scoped lang="scss">
.com-top-horizon-flex{
    display: flex;
}
</style>