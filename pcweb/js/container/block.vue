<template>
    <div class="com-block">
        <slot name="head">
            <div><b v-text="ctx.title"></b></div>
        </slot>

        <slot name="default">
            <div></div>
        </slot>
    </div>
</template>
<script>
    export default {
        props:{
            ctx:{
                default(){
                    return {}
                }
            }
        }
    }
</script>
<style scoped lang="scss">
.com-block {
    border: 1px solid #e5e5e5;
    background-color: white;
    margin: 5px;
    padding: 10px;
}
</style>