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
        <div>
            <component v-for="tab in ctx.tabs" :key="tab.label" v-show="is_show(tab)"
                       :is="tab.editor || tab._show_editor|| 'com-ui-blank'" :ctx="tab"></component>
        </div>

    </div>
</template>
<script>
    /*
    ctx={
       tabs:[
           {label:'标签页一','editor:'bbc'}:
       ]
    }
    * */
    export default {
        props:['ctx'],
        data(){
            return {
                crt_tab:this.ctx.tabs[0].label
            }
        },
        methods:{
            is_show(tab){
                if(this.crt_tab == tab.label){
                    Vue.set(tab,'_show_editor',tab.editor)
                    return true
                }else{
                    return false
                }
            },
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