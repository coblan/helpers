<template>
    <div class="com-top-footer-btn-pannel">
        <van-tabbar v-model="myactive" :fixed="false">
            <van-tabbar-item v-for="item in ctx.items" :icon="item.icon"  @click="on_click(item)" >
                <span v-text="item.label"></span>
            </van-tabbar-item>
        </van-tabbar>
        <!--<van-tabbar v-model="active" :fixed="false">-->
            <!--<van-tabbar-item icon="home-o" @click="on_click()">标签</van-tabbar-item>-->
            <!--<van-tabbar-item icon="search" dot>标签</van-tabbar-item>-->
            <!--<van-tabbar-item icon="friends-o" badge="5">标签</van-tabbar-item>-->
            <!--<van-tabbar-item icon="setting-o" badge="20">标签</van-tabbar-item>-->
        <!--</van-tabbar>-->
    </div>

</template>
<script>
    export default{
        props:['ctx'],
        data(){
            let active_index = this.ctx.items.indexOf(ex.findone(this.ctx.items,{name:this.ctx.active}))
          return {
              myactive:active_index
          }
        },
        methods:{
            on_click(item){
                if(item.action){
                    ex.eval(item.action,{head:item})
                }
//                live_root.open_live("live_html",{content:"<div style='height:800px'>hello world</div>"})
            }
        }
    }
</script>

<style scoped lang="scss">
    .com-top-footer-btn-pannel{
        position: absolute;
        /*top: calc( var(--app-height) - 50px);*/
        bottom: 0;
        left: 0;
        right: 0;
    }
</style>