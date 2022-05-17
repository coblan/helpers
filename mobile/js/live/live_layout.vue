<template>
    <div class="com-live-layout">

        <com-uis-nav-bar v-if="ctx.title" :title="ctx.title" :back="can_back" :ops="ctx.ops"></com-uis-nav-bar>
        <div class="body-content">
          <div style="display: contents" v-for="head in ctx.layout_editors">
            <component v-if="head.bind" :is="head.editor"  v-bind="head.bind"></component>
            <component v-else :is="head.editor" :ctx="head"></component>
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
        basename:'live-layout',
        data(){
            var childStore = new Vue()
            childStore.vc=this
            return {
                childStore:childStore
            }
        },
        computed:{
            can_back(){
                return this.$root.stack.length >1
            }
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
    .com-live-layout{
        background-color: #f9f9f9;
        height :var(--app-height);
        display: flex;
        flex-direction: column;
    }

    .body-content{
        overflow: auto;
        width: 100%;
        flex-grow: 10;
    }
</style>


