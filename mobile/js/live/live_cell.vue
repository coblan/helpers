<template>
    <div class="com-live-cell">
        <com-uis-nav-bar :title="ctx.title" :back="can_back" :back_action="ctx.back_action"></com-uis-nav-bar>
        <div v-if="ctx.groups">
            <van-cell-group :title="group.label" v-for="group in ctx.groups">
                <van-cell :title="cell.label" :is-link="has_link(cell)" v-for="cell in group.cells" @click="onclick(cell)" />
            </van-cell-group>
        </div>
        <div v-else>
            <van-cell :title="cell.label" :is-link="has_link(cell)" v-for="cell in ctx.cells" @click="onclick(cell)"/>
        </div>
       <component v-if="ctx.bottom_editors" v-for="item in ctx.bottom_editors" :is="item.editor" :ctx="item"></component>
    </div>


</template>
<script>
/*
*  --------------------
*  text            >
* --------------------
*
* 这个样子的页面
* */
    export default {
        props:['ctx'],
        basename:'live-cell',
        computed:{
            can_back(){
                return this.$root.stack.length >1
            }
        },
        methods:{
            has_link(cell){
                var click_express = cell.click_express || cell.action
                return click_express ? true : false
            },
            onclick(cell){
                var click_express = cell.click_express || cell.action
                if(cell.click_express){
                    ex.eval(cell.click_express,{head:cell})
                }
            },
        }
    }
</script>
<style scoped lang="scss">
    .com-live-cell{
        background-color: #f9f9f9;
    }
</style>