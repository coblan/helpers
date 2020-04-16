<template>
<div class="com-top-sidebar-ctn" :class="ctx.class">
    <van-sidebar v-model="activekey">
        <van-sidebar-item :title="tab.label" v-for="tab in ctx.tabs" />
    </van-sidebar>
    <div class="content">
        <component v-for="(tab,index) in ctx.tabs" :key="index" v-show="is_show(tab,index)"
                   :is="tab.show_editor|| 'com-ui-blank'" :ctx="tab"></component>
    </div>
</div>
</template>
<script>
 export default {
     props:['ctx'],
     data(){
         return {
             activekey:0
         }
     },
     mounted(){
         if(this.ctx.css){
             ex.append_css(this.ctx.css)
         }
     },
     methods:{
         is_show(tab,index){
            if(this.activekey==index){
                Vue.set(tab,'show_editor',tab.editor)
                return true
            }else{
                return false
            }
         }
     }
 }
</script>
<style lang="scss" scoped>
.com-top-sidebar-ctn{
    width: 100vw;
    display: flex;

    .content{
        background-color: white;
        height: 100%;
        flex-grow: 10;
    }

}
</style>