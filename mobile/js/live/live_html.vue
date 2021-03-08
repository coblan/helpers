<template>
    <div class="com-live-html">
        <com-uis-nav-bar :title="ctx.title" :back="can_back" :back_action="ctx.back_action"></com-uis-nav-bar>
        <div class="content" v-html="ctx.content">
        </div>

        <div v-if="ctx.footer" class="footer-content">
            <component :is="ctx.footer.editor"  :ctx="ctx.footer"></component>
        </div>
    </div>
</template>
<script>
    export default {
        props:['ctx'],
        basename:'live-html',
        computed:{
            can_back(){
                return this.$root.stack.length >1
            }
        },
    }
</script>

<style lang="scss">
    .com-live-html{
        background-color: white;
        display:flex;
        height: var(--app-height);
        flex-direction:column;

    .content{
        line-height: .5rem;
        padding: .3rem .2rem;
        /*height: calc( var(--app-height) - 80px );*/
        overflow: auto;

        img{
            max-width: 100%;
            height: auto;
        }
        }

    }

</style>
