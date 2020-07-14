<template>
    <div class="com-layout-vertical">
        <component v-for="item in ctx.items" :is="item.editor" :key="item.name" :ctx="item"></component>
    </div>
</template>
<script>
    export default {
        props:['ctx']
    }
</script>