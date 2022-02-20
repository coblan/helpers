<template>
    <span class="com-drop-btn" :class="my_ctx.class">
        <!--<el-button size="mini" :type="my_ctx.type" @click="on_click()"-->
                   <!--:title="ctx.title"-->
                   <!--:disabled="is_disabled" :plain="my_ctx.plain">-->
            <!--<slot name="content">-->
                <!--<i v-if="my_ctx.icon" :class="my_ctx.icon"></i>-->
                <!--<span v-text="my_ctx.label"></span>-->
            <!--</slot>-->
        <!--</el-button>-->

        <!--split-button :type="my_ctx.type"-->
        <el-dropdown trigger="click">
            <el-button  size="mini" :disabled="is_disabled">
               <span class="el-dropdown-link">
                 <span v-text="my_ctx.label"></span>
                  <i class="el-icon-arrow-down el-icon--right"></i>
              </span>
            </el-button>
            <el-dropdown-menu slot="dropdown" >
                <el-dropdown-item v-for="action in my_ctx.menu" :disabled="action_disable(action)">
                    <span :title="action.title" @click="on_click_action(action)" v-text="action.label"></span>
                </el-dropdown-item>
            </el-dropdown-menu>
        </el-dropdown>
    </span>
</template>
<script>
    export default {
        props:['ctx','head'],
        data(){
            return {
                parStore:ex.vueParStore(this),
                // TODO 剔除某些老组件后，需要移除 head的引用
                my_ctx:this.ctx?this.ctx:this.head,
            }
        },
        computed:{
            is_disabled(){
                if(this.my_ctx .disabled_express){
                    return  ex.eval(this.my_ctx.disabled_express,{ps:this.parStore})
                }else{
                    return false
                }
            }
        },
        mounted(){
            if(this.my_ctx.css){
                ex.append_css(this.my_ctx.css)
            }
        },
        methods:{
            action_disable(action){
                if(action.disabled_express){
                    return ex.eval(action.disabled_express,{ps:this.parStore})
                }else{
                    return false
                }
            },
//            on_group_click(){
//                this.on_click_action(this.my_ctx)
//            },
            on_click_action(action){
                if(action.click_express){

                    // 在table组件中，会先检查选中的row。
                    if(action.row_match){
                        var p = this.parStore.check_selected(action)
                    }else{
                        var p = Promise.resolve()
                    }
                    p.then(()=>{
                        ex.eval(action.click_express,{head:action,ps:this.parStore,vc:this})
                })
                }
            }
        }
    }
</script>

<style scoped lang="scss">
    .com-btn{
        margin: 0 1px;
    }
</style>