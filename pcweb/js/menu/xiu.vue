<template>
    <div :class="ctx.class" class="com-xiu-menu">
        <div class="stand"></div>
        <div class="fixed-xiu-menu" >
            <div class="web-wrap">
                <div class="brand" v-html="parStore.vc.head_bar_data.brand"></div>
                <div class="menu">
                    <div class="action"  v-for="action in ctx.menu">
                        <a v-if="action.url"  :class="{'active':is_active(action)}" :href="action.url" v-text="action.label"></a>
                        <a v-else :class="{'active':is_active(action)}"  href="#" @click="on_click(action)" v-text="action.label"></a>
                    </div>
                </div>
                <div class="right-ops">

                </div>

            </div>

        </div>
    </div>

</template>
<script>

    export default {
        props:['ctx'],
        data(){
            return {
                parStore:ex.vueParStore(this)
            }
        },
        mounted(){
            $(window).scroll(()=>{
                $(this.$el).css({
                'left': -$(window).scrollLeft()
                //Why this 15, because in the CSS, we have set left 15, so as we scroll, we would want this to remain at 15px left
                });
            });

        },
        methods:{
            on_click(action){
                ex.eval(action.action,{head:action})
            },
            is_active:function(action){
                if (action.url == location.pathname){
                    return true
                }else{
                    return false
                }
            },
        }
    }
</script>
<style scoped lang="stylus">
@import "./styl/xiu.styl"
</style>
<style scoped lang="scss">
.dark{
    .stand{
        height: 50px;
    }
    .fixed-xiu-menu{
        background-color: #303030;
        border-bottom:none;
        line-height:50px;
        height: 50px;
        .menu{
            .action{
                font-size:14px;
                a{
                    color:#b4b4b4;
                    &:hover,&.active{
                             color: #e35b0f;
                         }

                }
            }

        }
    }
 }



</style>
