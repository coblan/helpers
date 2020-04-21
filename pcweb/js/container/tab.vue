<template>
    <div class="com-ctn-tab">
        <div class="tab-bar">
            <div class="tab" :class="{active:crt_tab==tab.label}" @click="on_click(tab)" :key="tab.label" v-for="tab in ctx.tabs">
                <span class="myicon">
                     <img v-if="crt_tab==tab.label" :src="tab.icon_active" alt="">
                        <img v-else :src="tab.icon" alt="">
                </span>

                <span class="mylabel" v-text="tab.label"></span>
            </div>
        </div>

    </div>
</template>
<script>
    export default {
        props:['ctx'],
        data(){
            return {
                crt_tab:this.ctx.tabs[0].label
            }
        },
        methods:{
            on_click(tab){
                this.crt_tab = tab.label
            }
        }
    }
</script>
<style scoped lang="scss">
.tab-bar{
    display: flex;
}
    .tab{
        cursor: default;
        line-height: 1em;
        padding: 10px 30px;
        &.active{
             color: #0FAFA3;
         }
         .myicon{
             img{
                 height: 1.3em;
                 vertical-align:middle;
             }
         }
        .mylabel{
            display: inline-block;
            /*padding: 0 5px;*/
        }
    }
</style>