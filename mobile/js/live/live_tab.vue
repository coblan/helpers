<template>
    <div class="com-live-tab">
        <com-uis-nav-bar v-if="ctx.title" :title="ctx.title"  :back_action="ctx.back_action"></com-uis-nav-bar>
        <!--:back="can_back"-->
        <van-tabs v-model="active" class="tab-com">
            <van-tab v-for="(item,index) in ctx.items" :title="item.label">
                <div class="inn-wrap">
                    <component class="inn-content" :is="item.editor" :ctx="item"></component>
                </div>

            </van-tab>
        </van-tabs>
        <div v-if="ctx.footer" class="footer-content">
            <component :is="ctx.footer.editor"  :ctx="ctx.footer"></component>
        </div>

    </div>
</template>
<script>
    export default {
        props:['ctx'],
        basename:'live-tab',
        data(){
            return {
                value:'',
                active: 0,
            }
        },
        methods:{
            onSearch(){

            }
        }
    }
</script>
<style lang="scss" scoped>
    .com-live-tab{
        width: var(--app-width);
        height: var(--app-height );
        display: flex;
        flex-direction: column;
        .tab-com{
            flex-grow: 100;
            position: relative;
        }
        .inn-wrap{
            position: absolute;
            top:48px;
            left: 0;
            right: 0;
            bottom: 0;
            background-color: #fdfdfd;
            overflow: auto;
        }
    }
</style>