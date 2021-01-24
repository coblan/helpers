<template>
    <div class="com-live-tab">
        <com-uis-nav-bar v-if="ctx.title" :title="ctx.title"  :back_action="ctx.back_action"></com-uis-nav-bar>
        <!--:back="can_back"-->
        <van-tabs v-model="active">
            <van-tab v-for="(item,index) in ctx.items" :title="item.label">
                <component :is="item.editor" :ctx="item"></component>
            </van-tab>
        </van-tabs>
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
        width: 100vw;
        height: var(--app-height );
    }
</style>