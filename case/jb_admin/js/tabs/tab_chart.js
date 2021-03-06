require('./styl/tab_chart.styl')

var tab_chart={
    props:['tab_head','par_row'],
    data:function(){
        var vc = this
        var heads_ctx = this.tab_head.table_ctx
        var my_table_store ={
            data:function(){
                return {
                    head:heads_ctx,
                    heads:heads_ctx.heads,
                    row_filters:heads_ctx.row_filters,
                    row_sort:heads_ctx.row_sort,
                    director_name:heads_ctx.director_name,
                    footer:heads_ctx.footer || [],
                    ops:heads_ctx.ops || [],
                    rows:[],
                    row_pages:{},
                    selectable:heads_ctx.selectable==undefined? true:heads_ctx.selectable,
                    advise_heads:heads_ctx.advise_heads || [],
                    selected:[],
                    del_info:[],
                    search_args: {},
                    vc:vc,
                    parStore:ex.vueParStore(vc),
                    after_get_rows:heads_ctx.after_get_rows,
                    option:heads_ctx.option ||{}
                }
            },
            mixins:[table_store],
            methods:{
                switch_to_tab:function(kws){
                    if(window.root_live){
                        table_store.methods.switch_to_tab(kws)
                    }else{
                        this.parStore.switch_to_tab(kws)
                    }
                },
                getRows:function(){
                    if(vc.tab_head.pre_set){
                        var pre_set = ex.eval(vc.tab_head.pre_set,{par_row:vc.par_row,vc:vc,ps:this})
                        ex.assign(this.search_args,pre_set)
                    }
                    table_store.methods.getRows.call(this)
                },
            }
        }
        return {
            childStore:new Vue(my_table_store),
            parStore:ex.vueParStore(vc),
            loaded:false,
        }
    },
    mounted(){
        ex.vueEventRout(this,this.tab_head.event_slots)
        // 如果有复杂的需求，则被 table_store.init_express接管
        if(!this.childStore.head.init_express){
            this.childStore.search()
        }
        if(this.tab_head.css){
            ex.append_css(this.tab_head.css)
        }
    },
    methods:{
    },

    template:`<div class="com-tab-table com-tab-chart flex-v" style="position: absolute;top:0;left:0;bottom: 0;right:0;overflow: auto;padding-bottom: 1em;">
       <div v-if="childStore.row_filters.length > 0" style="background-color: #fbfbf8;padding: 8px 1em;border-radius: 4px;margin-top: 8px">
            <com-table-filters></com-table-filters>
        </div>
        <div  v-if="childStore.ops.length>0 ">
            <com-table-operations></com-table-operations>
        </div>

        <div v-if="childStore.parents.length>0">
            <com-table-parents></com-table-parents>
        </div>

        <div class="box box-success flex-v flex-grow" style="margin-bottom: 0">
            <div class="table-wraper flex-grow" style="position: relative;">
                <!--<com-table-rows></com-table-rows>-->
                <div style="position: absolute;top:0;left:0;bottom: 0;right:0;overflow-y: auto">
                       <div class="statistic-panel" v-if="tab_head.foot_heads">
                    <label class="title-label" v-text="childStore.footer._label"></label>
                        <div class="foot-item" v-for="head in tab_head.foot_heads">
                            <span v-text="childStore.footer[head.name]"></span><br>
                            <span v-text="head.label"></span>
                        </div>
                    </div>

                    <div class="chart-panel">
                        <component :class="tab_head.chart_class"  v-for="head in tab_head.chart_heads" :is="head.editor" :ctx="head"></component>
                    </div>
                </div>
            </div>
        </div>
        <!--<div style="background-color: white;">-->
            <!--<com-table-pagination></com-table-pagination>-->
        <!--</div>-->
    </div>`
}


Vue.component('com-tab-chart', function (resolve, reject) {
    ex.load_js(js_config.js_lib.echarts).then(()=>{
        resolve(tab_chart)
    })
})