<template>
    <div class="tab-full " style="position: absolute;bottom: 0;top: 0;left: 0;right: 0;" >
    aaa
        <el-tabs class="active-tab-hightlight-top"  v-if="tabs.length >1" type="border-card"
                  @tab-click="handleClick"
                  style="width: 100%;height: 100%;"
                  :value="crt_tab_name" >

              <el-tab-pane v-for="tab in normed_tab"
                         lazy
                         :key="tab.name"
                         :name="tab.name">
                        <span slot="label" v-if="tab.icon_image" class="tab-label" :class="{active:ctx.crt_tab_name==tab.name}">
                             <img class="icon_image_active" :src="tab.icon_image_active || tab.icon_image" alt="">
                             <img class="icon_image" :src=" tab.icon_image" alt="">
                            <span v-text="tab.label"></span>
                        </span>
                <span slot="label" v-else  v-text="tab.label" ></span>
                <component :is="tab.editor" :tab_head="tab"
                           :par_row="ctx.par_row"></component>


            </el-tab-pane>
        </el-tabs>

        <component v-else v-for="tab in tabs"  :is="tab.editor" :tab_head="tab"
                   :par_row="ctx.par_row" ></component>
    </div>
</template>
<script>
    export default {
        props:['ctx'],
        data(){
            var tabs=named_ctx[this.ctx.ctx_name]
            var childStore = new Vue()
            childStore.vc = this
            return {
                crt_tab_name:this.ctx.tab_name,
                tabs:tabs,
                childStore:childStore,
            }
        },
        computed:{
            normed_tab:function(){
                var tabs = this.tabs
                var par_row = this.ctx.par_row
                var out_tabs = ex.filter(tabs,function(tab){
                    if(tab.show_express){
                        return ex.eval(tab.show_express,{par_row:par_row})
                    }else{
                        return true
                    }
                })
                return out_tabs
            }
        },
        methods:{
            handleClick(tab, event) {
                if(this.crt_tab_name != tab.name){
                    this.crt_tab_name = tab.name
                    this.childStore.$emit('click-show',tab.name)
                }
            },
        }
    }
</script>