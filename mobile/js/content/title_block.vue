<template>
    <div class="com-title-block" :class="ctx.class">
        <slot name="title">
            <div class="title" v-text="ctx.title"></div>
            <div class="sub-title" v-text="ctx.sub_title"></div>
        </slot>
        <slot name="content">
            <div class="normal" v-html="ctx.html"></div>
        </slot>
    </div>
</template>

<script>
    export default {
        props:['ctx'],
        data(){
            var childStore = new Vue()
            childStore.vc=this
            return {
                childStore:childStore
            }
        },
        mounted(){
            if(this.ctx.css){
                ex.append_css(this.ctx.css)
            }
        }
    }
</script>

<style scoped lang="scss">
    .title{
        text-align: center;
        font-size: .4rem;
        font-weight: bold;
        margin: .3rem;
    }
    .sub-title{
        text-align: center;
        color: grey;
        font-size: .26rem;
    }
.normal{
    padding: .3rem;
    line-height: .4rem;
}
</style>