<template>
    <div class="com-field-head-shower">
        <div class="readonly-info" v-html='head.html'></div>
    </div>
</template>
<script>
    export default {
        props:['row','head']
    }
</script>
<style scoped lang="scss">
.com-field-head-shower{
    font-size: 12px;
    color: #797979;
}
</style>