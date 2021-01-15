
<template>
    <div class="com-live-page">
        <div v-if="ctx.head" class="head-content">
            <component :is="ctx.head.editor"  :ctx="ctx.head"></component>
        </div>

        <div class="body-content">
            <div class="body-inn">
                <component :is="head.editor" v-for="head in ctx.layout_editors" :ctx="head"></component>
            </div>

        </div>
        <div v-if="ctx.footer" class="footer-content">
            <component :is="ctx.footer.editor"  :ctx="ctx.footer"></component>
        </div>


    </div>
</template>
<script>
    export default {
        props:['ctx'],
        basename:'live-page',
        data(){
            var childStore = new Vue()
            childStore.vc=this
            return {
                childStore:childStore
            }
        },
        computed:{
//            can_back(){
//                return this.$root.stack.length >1
//            }
        },
        deactivated(){
            this.scroll = $(this.$el).find('.com-fileds-panel').scrollTop()
        },
        activated() {
            if( this.scroll){
                var count =0
                var index =  setInterval(()=>{
                            $(this.$el).find('.com-fileds-panel').scrollTop( this.scroll)
                count+=30
                if(count > 160){
                    clearInterval(index)
                }
            },30)
            }
        },
    }
</script>

<style scoped lang="scss">
.com-live-page{
    background-color:#f9f9f9;
    min-height: var(--app-height);
    display: flex;
    flex-direction: row;

    .body-content{
        flex-grow: 100;
        width: 100%;
    }
    .body-inn{
        position: absolute;
        top:0;
        left: 0;
        right: 0;
        bottom: 0;
        overflow: auto;
    }
}
</style>