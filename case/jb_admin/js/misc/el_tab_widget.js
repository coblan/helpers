Vue.component('com-widget-el-tab',{
    props:['ctx'],
    template:`<div class="tab-full active-tab-hightlight-top" style="position: absolute;bottom: 0;top: 0;left: 0;right: 0;" >
     <el-tabs  v-if="ctx.tabs.length >1" type="border-card"
                           @tab-click="handleClick"
                           style="width: 100%;height: 100%;"
                           :value="ctx.crt_tab_name" >

                    <!--<el-tab-pane v-for="tab in normed_tab( tabgroup.tabs )"-->
                    <el-tab-pane v-for="tab in normed_tab"
                                lazy
                                 :key="tab.name"
                                 :name="tab.name">
                        <span slot="label" v-text="tab.label" ></span>

                        <component :is="tab.com" :tab_head="tab"
                                   :par_row="ctx.par_row"
                                   :ref="'_tab_'+tab.name" @tab-event="up_event($event)"></component>


                    </el-tab-pane>
                </el-tabs>

                <component v-else v-for="tab in ctx.tabs"  :is="tab.com" :tab_head="tab"
                           :par_row="ctx.par_row"
                           :ref="'_tab_'+tab.name" @tab-event="up_event($event)"></component>
    </div>`,
   watch:{
       'ctx.crt_tab_name':function (v){
            this.show_tab(v)
        }
   },
    mounted:function(){
        this.show_tab(this.ctx.crt_tab_name)
    },
    computed:{
        normed_tab:function(){
            var tabs = this.ctx.tabs
            var par_row = this.ctx.par_row
            var out_tabs = ex.filter(tabs,function(tab){
            if(tab.show){
                return ex.eval(tab.show,{par_row:par_row})
                //return ex.boolExpress(par_row,tab.show)
                }else{
                    return true
                }
            })
            return out_tabs
        }
    },
    methods:{
        show_tab:function(name){
            this.ctx.crt_tab_name=name
            //this.crt_tab_name = name
            //var self =this
            //Vue.nextTick(function(){
            //    self.$refs['_tab_'+name][0].on_show()
            //})
        },
        handleClick(tab, event) {
            this.show_tab(tab.name)
        },
        up_event:function(event){
            this.$emit('win-event',event)
        }
    }
})