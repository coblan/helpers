<template>
    <div class="com-block-title-plain">
        <div v-if="ctx.title" class="title" v-text="ctx.title"> </div>
        <div v-if="ctx.sub_title" class="sub-title" v-text="ctx.sub_title"></div>
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

<style scoped lang="scss">
.com-block-title-plain{
    text-align: center;
}
</style>