
var live_table_chart={
props:['ctx'],
basename:'live-table-chart',
data:function(){
    var vc = this
    //var heads_ctx = this.ctx
    var my_table_store ={
        data:function(){
            return {
                head:vc.ctx,
                heads:vc.ctx.heads,
                row_filters:vc.ctx.row_filters,
                row_sort:vc.ctx.row_sort,
                director_name:vc.ctx.director_name,
                footer:vc.ctx.footer || [],
                ops:vc.ctx.ops || [],
                rows: vc.ctx.rows || [] ,
                row_pages:vc.ctx.row_pages || {},
                selectable:vc.ctx.selectable==undefined? true:vc.ctx.selectable,
                selected:[],
                del_info:[],
                search_args: vc.ctx.search_args || {},
                vc:vc,
                parStore:ex.vueParStore(vc)
            }
        },
        mixins:[table_store],
        watch:{
            search_args:function(v){
                console.log(v)
            }
        },
        methods:{
        }
    }
    return {
        childStore:new Vue(my_table_store),
        parStore:ex.vueParStore(vc),
    }
},
mounted:function(){
    if(this.ctx.event_slots){
        ex.vueEventRout(this,this.ctx.event_slots)
    }
    if(this.ctx.autoload){
        this.childStore.search().then(()=>{
            this.draw()
        })
    }


},
    methods:{
        draw(){
            ex.each(this.ctx.charts,item=>{
                this.draw_item(item)
            })
        },
        draw_item(item){
            debugger
            var myChart = echarts.init( $(this.$el).find('.mychart-'+item.name)[0] );

            // 指定图表的配置项和数据
            var option = {
                title: {
                    text: ''
                },
                tooltip: {},
                legend: {
                    data:['用户数']
                },
                xAxis: {
                    data: this.parStore.rows.map(item=>{return item.starttime}).reverse()
                    //data: ["衬衫","羊毛衫","雪纺衫","裤子","高跟鞋","袜子"]
                },
                yAxis: {},
                series: [{
                    name: '用户数',
                    type: 'bar',
                    data: this.parStore.rows.map(item=>{return item.betusernum}).reverse(),
                    barMaxWidth: 30,
                    itemStyle: {
                        normal: {
                            color:'#27B6AC'
                        },
                    },

                }]
            };

            // 使用刚指定的配置项和数据显示图表。
            myChart.setOption(option);
        }
    },

template:`<div class="live-table live-table-chart flex-v" style="position: absolute;top:0;left:0;bottom: 0;right:0;overflow: auto;padding-bottom: 2px;">
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

            <!--<component :is="ctx.inn_editor"></component>-->
            <div class="mychart" :class="'mychart-'+item.name" v-for="item in ctx.charts"></div>

        </div>
    </div>
    <!--<div style="background-color: white;">-->
        <!--<com-table-pagination></com-table-pagination>-->
    <!--</div>-->
</div>`
}


window.live_table_chart = live_table_chart

Vue.component('com-table-chart',function(resolve,reject){
    ex.load_js(js_config.js_lib.echarts).then(function(){
        resolve(live_table_chart)
    })
})

//Vue.component('com-live-table-type',live_table_type)
