
var el_tab = {
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
                        <!--<span v-if="!tab._loaded"></span>-->
                        <component :is="tab.editor || tab.com " :tab_head="tab"
                                   :par_row="ctx.par_row"
                                   :ref="'_tab_'+tab.name" @tab-event="up_event($event)"></component>


                    </el-tab-pane>
                </el-tabs>

                <component v-else v-for="tab in ctx.tabs"  :is="tab.editor || tab.com " :tab_head="tab"
                           :par_row="ctx.par_row"
                           :ref="'_tab_'+tab.name" @tab-event="up_event($event)"></component>
    </div>`,
    data(){
        //ex.each(this.ctx.tabs,tab=>{
        //    if(tab.lazy_init){
        //        Vue.set(tab,'_loaded',false)
        //    }
        //})
        return {
            is_mounted:false
        }
    },
   watch:{
       //'ctx.crt_tab_name':function (v){
       //     this.show_tab(v)
       // }
   },
    created(){

    },
    mounted:function(){
        this.is_mounted  = true
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
        show_tab(name){
            //var tab_head = ex.findone(this.normed_tab,{name:name})
            //if(tab_head.lazy_init){
            //     ex.eval(tab_head.lazy_init,{head:tab_head}).then(()=>{
            //         delete tab_head.lazy_init
            //         Vue.set(tab_head,'_loaded',true)
            //         this.ctx.crt_tab_name=name
            //     })
            //
            //}else{
            //    Vue.set(tab_head,'_loaded',true)
            //
            //}
            this.ctx.crt_tab_name=name

            //var self =this
            //if(this.is_mounted){
            //    Vue.nextTick(function(){
            //        if(self.$refs['_tab_'+name][0].on_show){
            //            self.$refs['_tab_'+name][0].on_show()
            //        }
            //    })
            //}
        },
        handleClick(tab, event) {
            this.show_tab(tab.name)
        },
        up_event:function(event){
            this.$emit('win-event',event)
        }
    }
}
Vue.component('com-widget-el-tab',el_tab)
window.live_el_tab = el_tab